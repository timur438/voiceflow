import json
import subprocess
import os
import base64
import asyncio
import datetime
from typing import Optional, List
from pydantic import BaseModel
import tempfile
import torch
import torchaudio
from pyannote.audio import Pipeline
from queue import Queue
from threading import Thread, Lock
import time
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("predictor.log"),
        logging.StreamHandler()
    ]
)

class TranscriptionSegment(BaseModel):
    text: str
    start: float
    end: float
    speaker: str
    words: Optional[List[dict]] = None

class TranscriptionResult(BaseModel):
    segments: List[TranscriptionSegment]
    language: str
    num_speakers: int
    text: str
    translation: Optional[str] = None

class TranscriptionQueue:
    def __init__(self, max_concurrent=2):
        self.queue = Queue()
        self.max_concurrent = max_concurrent
        self.current_tasks = 0
        self.lock = Lock()
        self.worker = Thread(target=self._process_queue, daemon=True)
        self.worker.start()

    def add_task(self, task):
        return self.queue.put(task)

    def _process_queue(self):
        while True:
            task = self.queue.get()
            with self.lock:
                while self.current_tasks >= self.max_concurrent:
                    time.sleep(1)
                self.current_tasks += 1
            
            try:
                task()
            finally:
                with self.lock:
                    self.current_tasks -= 1
                self.queue.task_done()

class Predictor:
    def setup(self):
        logging.info("Setting up Predictor...")
        self.model_path = "./whisper.cpp/models/ggml-large-v3-turbo.bin"
        if not os.path.exists(self.model_path):
            logging.info("Model not found, downloading...")
            self._download_model("large-v3-turbo")

        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            raise RuntimeError("Hugging Face auth token is missing")
        
        logging.info("Initializing speaker diarization pipeline...")
        self.diarization_pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=hf_token
        ).to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

        self.transcription_queue = TranscriptionQueue(max_concurrent=3)

    def _download_model(self, model_name):
        logging.info(f"Downloading model: {model_name}")
        subprocess.run([
            "bash", "./whisper.cpp/models/download-ggml-model.sh", model_name
        ], check=True)

    def _convert_to_wav(self, input_file: str) -> str:
        output_file = f"{tempfile.mktemp()}.wav"
        logging.info(f"Converting {input_file} to WAV: {output_file}")
        try:
            subprocess.run([
                "ffmpeg", "-i", input_file, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", output_file
            ], check=True, capture_output=True)
            return output_file
        except subprocess.CalledProcessError as e:
            logging.error(f"FFmpeg error: {e.stderr.decode()}")
            raise RuntimeError(f"FFmpeg error: {e.stderr.decode()}")
        finally:
            if os.path.exists(input_file):
                os.remove(input_file)
                logging.info(f"Removed input file: {input_file}")


    def _get_speaker_segments(self, audio_path, num_speakers=None):
        logging.info(f"Running speaker diarization on {audio_path}")
        try:
            waveform, sample_rate = torchaudio.load(audio_path)
            with torch.cuda.device('cuda' if torch.cuda.is_available() else 'cpu'):
                diarization = self.diarization_pipeline(
                    {"waveform": waveform, "sample_rate": sample_rate}, num_speakers=num_speakers
                )
            speaker_segments = [
                {"start": turn.start, "end": turn.end, "speaker": speaker}
                for turn, _, speaker in diarization.itertracks(yield_label=True)
            ]
            logging.info(f"Detected {len(set(s['speaker'] for s in speaker_segments))} speakers")

            del diarization
            torch.cuda.empty_cache()

            return speaker_segments, len(set(s['speaker'] for s in speaker_segments))
        except Exception as e:
            logging.error(f"Diarization error: {str(e)}")
            raise RuntimeError(f"Diarization error: {str(e)}")

    def _process_audio(self, wav_file: str, language: str = "ru", translate: bool = False) -> dict:
        logging.info(f"Processing audio with Whisper: {wav_file}")
        output_json = tempfile.mktemp(suffix=".json")
        command = [
            "./whisper.cpp/build-cuda/bin/whisper-cli",
            "-m", self.model_path, "-f", wav_file,
            "--output-json", "--print-progress"
        ]
        if language:
            command.extend(["--language", language])
        if translate:
            command.append("--translate")
        command.extend(["-of", output_json[:-5]])

        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                logging.error(f"Whisper error: {stderr}")
                raise Exception(f"Whisper process failed: {stderr}")
            
            with open(output_json, 'r') as f:
                result = json.load(f)
                
            logging.info(f"Whisper result: {result}")
            
            # Преобразуем формат вывода в нужную структуру
            if "transcription" in result:
                segments = []
                for trans in result["transcription"]:
                    # Преобразуем миллисекунды в секунды
                    start = trans["offsets"]["from"] / 1000.0
                    end = trans["offsets"]["to"] / 1000.0
                    
                    segments.append({
                        "text": trans["text"].strip(),
                        "start": start,
                        "end": end,
                        "words": []  # если нужно, можно добавить обработку слов
                    })
                
                return {
                    "segments": segments,
                    "language": result.get("result", {}).get("language", "auto")
                }
            else:
                logging.error(f"Unexpected result format: {result}")
                raise Exception("Unexpected result format")
                
        finally:
            if os.path.exists(output_json):
                os.remove(output_json)

    def _merge_segments(self, segments):
        """Объединяет сегменты в осмысленные группы по спикерам"""
        merged = []
        current = None
        
        for seg in segments:
            # Пропускаем пустые сегменты
            if not seg["text"] or seg["text"].isspace():
                continue

            if not current:
                current = {
                    "text": seg["text"],
                    "start": seg["start"],
                    "end": seg["end"],
                    "speaker": seg["speaker"],
                    "words": seg.get("words", [])
                }
                continue

            # Если тот же спикер и промежуток между сегментами меньше 1 секунды
            if (seg["speaker"] == current["speaker"] and 
                (seg["start"] - current["end"]) < 1.0):
                
                # Проверяем, что текущий текст не пустой
                if current["text"] and seg["text"]:
                    # Убираем пробел в начале, если это часть слова
                    if (len(current["text"]) > 0 and 
                        len(seg["text"]) > 0 and 
                        current["text"][-1].isalpha() and 
                        seg["text"][0].isalpha()):
                        current["text"] += seg["text"]
                    else:
                        current["text"] += " " + seg["text"].lstrip()
                else:
                    # Если один из текстов пустой, просто используем непустой
                    current["text"] = current["text"] or seg["text"]
                
                current["end"] = seg["end"]
                if seg.get("words"):
                    current["words"].extend(seg["words"])
            else:
                # Очищаем текст от лишних пробелов и знаков препинания
                current["text"] = current["text"].strip()
                if current["text"] and not current["text"].isspace():
                    merged.append(current)
                current = {
                    "text": seg["text"],
                    "start": seg["start"],
                    "end": seg["end"],
                    "speaker": seg["speaker"],
                    "words": seg.get("words", [])
                }

        # Добавляем последний сегмент, если он существует и не пустой
        if current and current["text"] and current["text"].strip() and not current["text"].isspace():
            merged.append(current)

        return merged

    async def predict(self, file_string: str, num_speakers: int = None, translate: bool = False, language: str = "ru", group_segments: bool = False) -> TranscriptionResult:
        temp_input = tempfile.mktemp()
        wav_file = None
        try:
            logging.info("Decoding input file...")
            with open(temp_input, "wb") as f:
                f.write(base64.b64decode(file_string))
            wav_file = self._convert_to_wav(temp_input)
            future_result = {}
            def process_task():
                try:
                    speaker_segments, detected_speakers = self._get_speaker_segments(wav_file, num_speakers)
                    result = self._process_audio(wav_file, language, translate)
                    
                    # Создаем предварительные сегменты
                    raw_segments = [
                        {
                            "text": seg["text"].strip(),
                            "start": seg["start"],
                            "end": seg["end"],
                            "speaker": next((s["speaker"] for s in speaker_segments if s["start"] <= (seg["start"] + seg["end"]) / 2 <= s["end"]), "UNKNOWN"),
                            "words": seg.get("words", [])
                        }
                        for seg in result["segments"]
                    ]
                    
                    # Объединяем сегменты
                    merged_segments = self._merge_segments(raw_segments)
                    
                    # Создаем финальные TranscriptionSegment объекты
                    segments = [TranscriptionSegment(**seg) for seg in merged_segments]
                    
                    transcription_result = TranscriptionResult(
                        segments=segments,
                        language=result.get("language", "auto"),
                        num_speakers=detected_speakers,
                        text=" ".join([s.text for s in segments]),
                        translation=None
                    )
                    
                    output_filename = os.path.join("temp_files", f"transcription_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                    with open(output_filename, "w") as f:
                        json.dump(transcription_result.dict(), f, indent=4, ensure_ascii=False)
                    logging.info(f"Saved transcription: {output_filename}")
                    future_result['result'] = transcription_result
                except Exception as e:
                    logging.error(f"Prediction error: {str(e)}")
                    future_result['error'] = e
            
            self.transcription_queue.add_task(process_task)
            while 'result' not in future_result and 'error' not in future_result:
                await asyncio.sleep(0.1)
            if 'error' in future_result:
                raise future_result['error']
            return future_result['result']
        finally:
            if os.path.exists(temp_input):
                os.remove(temp_input)
            if wav_file and os.path.exists(wav_file):
                os.remove(wav_file)

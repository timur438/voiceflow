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

load_dotenv()

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
        self.model_path = "./whisper.cpp/models/ggml-large-v3-turbo.bin"
        if not os.path.exists(self.model_path):
            self._download_model("large-v3-turbo")

        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            raise RuntimeError("Hugging Face auth token is missing")
            
        self.diarization_pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=hf_token
        ).to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

        self.transcription_queue = TranscriptionQueue(max_concurrent=3)

    def _download_model(self, model_name):
        subprocess.run([
            "bash",
            "./whisper.cpp/models/download-ggml-model.sh",
            model_name
        ], check=True)

    def _convert_to_wav(self, input_file: str) -> str:
        output_file = f"{tempfile.mktemp()}.wav"
        try:
            subprocess.run([
                "ffmpeg",
                "-i", input_file,
                "-ar", "16000",
                "-ac", "1",
                "-c:a", "pcm_s16le",
                output_file
            ], check=True, capture_output=True)
            return output_file
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg error: {e.stderr.decode()}")

    def _get_speaker_segments(self, audio_path, num_speakers=None):
        """Получение сегментов с информацией о спикерах"""
        try:
            waveform, sample_rate = torchaudio.load(audio_path)
            
            # Освобождаем память GPU после использования
            with torch.cuda.device('cuda' if torch.cuda.is_available() else 'cpu'):
                diarization = self.diarization_pipeline(
                    {"waveform": waveform, "sample_rate": sample_rate},
                    num_speakers=num_speakers
                )
                
                speaker_segments = []
                for turn, _, speaker in diarization.itertracks(yield_label=True):
                    speaker_segments.append({
                        "start": turn.start,
                        "end": turn.end,
                        "speaker": speaker
                    })
                
                num_speakers = len(set(s["speaker"] for s in speaker_segments))
                
                # Явно освобождаем память
                del diarization
                torch.cuda.empty_cache()
                
                return speaker_segments, num_speakers
        except Exception as e:
            raise RuntimeError(f"Diarization error: {str(e)}")

    def _process_audio(self, wav_file: str, language: str = "ru", translate: bool = False) -> dict:
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model file not found: {self.model_path}")
            
            if not os.path.exists(wav_file):
                raise FileNotFoundError(f"WAV file not found: {wav_file}")

            command = [
                "./whisper.cpp/build-cuda/bin/whisper-cli",
                "-m", self.model_path,
                "-f", wav_file,
                "--output-json",
                "--print-progress",
                "--max-len", "1"
            ]

            if language:
                command.extend(["--language", language])
            if translate:
                command.append("--translate")

            output_json = f"{tempfile.mktemp()}"
            command.extend(["-of", output_json])

            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()

                if process.returncode != 0:
                    error_message = f"Whisper process failed with code {process.returncode}: {stderr}"
                    print(error_message)
                    raise Exception(error_message)

                with open(output_json, 'r') as f:
                    return json.load(f)

            finally:
                if os.path.exists(output_json):
                    os.remove(output_json)

        except Exception as e:
            raise Exception(f"Error processing audio: {str(e)}")

    async def predict(
            self,
            file_string: str = None,
            group_segments: bool = True,
            transcript_output_format: str = "both",
            num_speakers: int = None,
            translate: bool = False,
            language: str = "ru",
            prompt: str = None,
            summary_type: str = "summary",
            offset_seconds: int = 0,
        ) -> TranscriptionResult:
            temp_input = None
            wav_file = None
            
            try:
                temp_input = tempfile.mktemp()
                with open(temp_input, "wb") as f:
                    f.write(base64.b64decode(file_string))

                wav_file = self._convert_to_wav(temp_input)

                future_result = {}
                
                def process_task():
                    try:
                        speaker_segments, detected_speakers = self._get_speaker_segments(
                            wav_file, 
                            num_speakers
                        )

                        result = self._process_audio(wav_file, language, translate)

                        segments = []
                        full_text = []

                        for segment in result["segments"]:
                            text = segment["text"].strip()
                            full_text.append(text)

                            segment_center = (segment["start"] + segment["end"]) / 2
                            current_speaker = "UNKNOWN"
                            
                            for sp_segment in speaker_segments:
                                if sp_segment["start"] <= segment_center <= sp_segment["end"]:
                                    current_speaker = sp_segment["speaker"]
                                    break

                            segments.append(TranscriptionSegment(
                                text=text,
                                start=segment["start"],
                                end=segment["end"],
                                speaker=current_speaker,
                                words=segment.get("words", [])
                            ))

                        transcription_result = TranscriptionResult(
                            segments=segments,
                            language=result.get("language", "auto"),
                            num_speakers=detected_speakers,
                            text=" ".join(full_text),
                            translation=None
                        )
                        
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_filename = f"transcription_result_{timestamp}.json"
                        with open(output_filename, "w") as f:
                            json.dump(transcription_result.dict(), f, indent=4, ensure_ascii=False)
                        print(f"Результат транскрипции сохранен в файл: {output_filename}")

                        future_result['result'] = transcription_result
                    except Exception as e:
                        future_result['error'] = e

                self.transcription_queue.add_task(process_task)
                
                while 'result' not in future_result and 'error' not in future_result:
                    await asyncio.sleep(0.1)

                if 'error' in future_result:
                    raise future_result['error']

                return future_result['result']

            finally:
                # Очистка временных файлов
                #if temp_input and os.path.exists(temp_input):
                #    os.remove(temp_input)
                if wav_file and os.path.exists(wav_file):
                    os.remove(wav_file)

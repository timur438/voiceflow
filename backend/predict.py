import subprocess
import os
import base64
from typing import Optional, List
from pydantic import BaseModel
import tempfile
from ctypes import *
import torch
import torchaudio
from pyannote.audio import Pipeline

class TranscriptionSegment(BaseModel):
    text: str
    start: float
    end: float
    speaker: str  # Добавлен speaker
    words: Optional[List[dict]] = None

class TranscriptionResult(BaseModel):
    segments: List[TranscriptionSegment]
    language: str
    num_speakers: int  # Теперь обязательное поле
    text: str
    translation: Optional[str] = None

class Predictor:
    def setup(self):
        """Инициализация моделей"""
        # Инициализация whisper.cpp
        lib_path = os.path.join(os.path.dirname(__file__), "whisper.cpp/build/libwhisper.so")
        self.whisper_lib = CDLL(lib_path)
        
        self.model_path = "models/ggml-medium.bin"
        if not os.path.exists(self.model_path):
            self._download_model("medium")
            
        self.ctx = self.whisper_lib.whisper_init_from_file(self.model_path.encode('utf-8'))

        # Инициализация модели диаризации
        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            raise RuntimeError("Hugging Face auth token is missing")
            
        self.diarization_pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=hf_token
        ).to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    def _convert_to_wav(input_file: str) -> str:
        """Конвертация аудио в WAV формат"""
        output_file = f"{tempfile.mktemp()}.wav"
        try:
            subprocess.run([
                "ffmpeg",
                "-i", input_file,
                "-ar", "16000",  # частота дискретизации 16kHz
                "-ac", "1",      # моно
                "-c:a", "pcm_s16le",  # 16-bit PCM
                output_file
            ], check=True, capture_output=True)
            return output_file
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg error: {e.stderr.decode()}")

    def _get_speaker_segments(self, audio_path, num_speakers=None):
        """Получение сегментов с информацией о спикерах"""
        waveform, sample_rate = torchaudio.load(audio_path)
        diarization = self.diarization_pipeline(
            {"waveform": waveform, "sample_rate": sample_rate},
            num_speakers=num_speakers
        )
        
        # Преобразование результатов диаризации в удобный формат
        speaker_segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            speaker_segments.append({
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker
            })
            
        return speaker_segments, len(set(s["speaker"] for s in speaker_segments))

    def _assign_speakers_to_segments(self, transcribed_segments, speaker_segments):
        """Присваивание спикеров транскрибированным сегментам"""
        for segment in transcribed_segments:
            # Находим спикера, который говорил большую часть сегмента
            segment_center = (segment["start"] + segment["end"]) / 2
            relevant_speakers = []
            
            for sp_segment in speaker_segments:
                if (sp_segment["start"] <= segment_center <= sp_segment["end"]):
                    relevant_speakers.append(sp_segment["speaker"])
            
            segment["speaker"] = relevant_speakers[0] if relevant_speakers else "UNKNOWN"
        
        return transcribed_segments

    def predict(
        self,
        file_string: str = None,
        group_segments: bool = True,
        transcript_output_format: str = "both",
        num_speakers: int = None,
        translate: bool = False,
        language: str = None,
        prompt: str = None,
        summary_type: str = "summary",
        offset_seconds: int = 0,
    ) -> TranscriptionResult:
        temp_input = None
        wav_file = None
        
        try:
            # Декодирование и конвертация в WAV
            temp_input = tempfile.mktemp()
            with open(temp_input, "wb") as f:
                f.write(base64.b64decode(file_string))

            wav_file = self._convert_to_wav(temp_input)

            # Получение информации о спикерах
            speaker_segments, detected_speakers = self._get_speaker_segments(
                wav_file, 
                num_speakers
            )

            # Настройка параметров whisper
            params = self.whisper_lib.whisper_full_default_params(
                self.whisper_lib.WHISPER_SAMPLING_GREEDY
            )
            
            params.print_progress = False
            params.print_timestamps = True
            params.translate = translate
            if language:
                params.language = language.encode('utf-8')
            params.n_threads = 4
            params.token_timestamps = True
            
            # Транскрипция
            result = self.whisper_lib.whisper_full(
                self.ctx,
                params,
                wav_file.encode('utf-8'),
                None
            )

            # Получение результатов
            segments = []
            n_segments = self.whisper_lib.whisper_full_n_segments(self.ctx)
            full_text = []
            
            for i in range(n_segments):
                text = self.whisper_lib.whisper_full_get_segment_text(self.ctx, i)
                start = self.whisper_lib.whisper_full_get_segment_t0(self.ctx, i)
                end = self.whisper_lib.whisper_full_get_segment_t1(self.ctx, i)
                
                words = []
                if transcript_output_format in ("words_only", "both"):
                    n_tokens = self.whisper_lib.whisper_full_n_tokens(self.ctx, i)
                    for j in range(n_tokens):
                        word = self.whisper_lib.whisper_full_get_token_text(self.ctx, i, j)
                        t0 = self.whisper_lib.whisper_full_get_token_t0(self.ctx, i, j)
                        t1 = self.whisper_lib.whisper_full_get_token_t1(self.ctx, i, j)
                        
                        words.append({
                            "word": word.decode('utf-8'),
                            "start": t0,
                            "end": t1
                        })

                segment_text = text.decode('utf-8')
                full_text.append(segment_text)
                
                segments.append({
                    "text": segment_text,
                    "start": start,
                    "end": end,
                    "words": words if words else None
                })

            # Присваивание спикеров сегментам
            segments = self._assign_speakers_to_segments(segments, speaker_segments)
            
            detected_language = self.whisper_lib.whisper_full_get_detected_language(self.ctx)
            
            return TranscriptionResult(
                segments=[TranscriptionSegment(**s) for s in segments],
                language=detected_language.decode('utf-8'),
                num_speakers=detected_speakers,
                text=" ".join(full_text),
                translation=None
            )

        except Exception as e:
            raise RuntimeError(f"Transcription error: {str(e)}")

        finally:
            # Очистка временных файлов
            if temp_input and os.path.exists(temp_input):
                os.remove(temp_input)
            if wav_file and os.path.exists(wav_file):
                os.remove(wav_file)


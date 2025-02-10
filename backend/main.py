from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import base64
from predict import Predictor, TranscriptionResult, TranscriptionSegment

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["voiceflow.ru"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация предиктора при старте приложения
predictor = Predictor()
predictor.setup()

class SpeakerSegment(BaseModel):
    text: str
    start: float
    end: float
    speaker: str
    words: Optional[List[dict]] = None

class TranscriptionResponse(BaseModel):
    segments: List[SpeakerSegment]
    num_speakers: int
    language: str

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(file: UploadFile = File(...)):
    try:
        MAX_FILE_SIZE = 1000 * 1024 * 1024  # 1000MB в байтах
        file_size = 0
        file_content = bytearray()
        
        while chunk := await file.read(1024 * 1024):  # Чтение по 1MB
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=413,
                    detail="File size too large. Maximum size is 1000MB"
                )
            file_content.extend(chunk)

        response = JSONResponse(
            status_code=202,
            content={"message": "File accepted for processing"}
        )

        # Конвертация в base64
        file_string = base64.b64encode(file_content).decode('utf-8')

        result: TranscriptionResult = await predictor.predict(
            file_string=file_string,
            group_segments=True,
            transcript_output_format="both",  # получаем и текст, и слова
            num_speakers=None,  # автоопределение количества спикеров
            translate=False,
            language=None,  # автоопределение языка
        )

        # Формирование ответа
        response = TranscriptionResponse(
            segments=[
                SpeakerSegment(
                    text=segment.text,
                    start=segment.start,
                    end=segment.end,
                    speaker=segment.speaker,
                    words=segment.words
                ) for segment in result.segments
            ],
            num_speakers=result.num_speakers,
            language=result.language
        )

        return response

    except Exception as e:
        import traceback
        error_details = f"Error processing file: {str(e)}\n{traceback.format_exc()}"
        print(error_details) 
        raise HTTPException(
            status_code=500,
            detail=error_details
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

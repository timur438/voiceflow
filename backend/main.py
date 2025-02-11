from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import base64
from predict import Predictor, TranscriptionResult

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["voiceflow.ru"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

async def process_transcription(file_content: bytes):
    try:
        file_string = base64.b64encode(file_content).decode("utf-8")
        print("Файл конвертирован в base64, начало обработки...")
        
        result: TranscriptionResult = await predictor.predict(
            file_string=file_string,
            group_segments=True,
            transcript_output_format="both",
            num_speakers=None,
            translate=False,
            language=None,
        )
        
        print("Файл успешно обработан:")
        print(f"Язык: {result.language}, Спикеров: {result.num_speakers}")
        for segment in result.segments:
            print(f"[{segment.start}-{segment.end}] {segment.speaker}: {segment.text}")

    except Exception as e:
        print(f"Ошибка обработки: {str(e)}")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    try:
        print(f"Получен файл: {file.filename}, content_type: {file.content_type}")
        
        MAX_FILE_SIZE = 1000 * 1024 * 1024
        file_size = 0
        file_content = bytearray()
        
        while chunk := await file.read(1024 * 1024):
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                raise HTTPException(status_code=413, detail="File size too large. Maximum size is 1000MB")
            file_content.extend(chunk)
        
        print(f"Размер файла: {file_size} bytes")

        response = JSONResponse(status_code=202, content={"message": "File accepted for processing"})
        
        background_tasks.add_task(process_transcription, bytes(file_content))

        return response

    except Exception as e:
        import traceback
        error_details = f"Ошибка обработки файла: {str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_details)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
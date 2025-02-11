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

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        print(f"Получен файл: {file.filename}, content_type: {file.content_type}")
        
        MAX_FILE_SIZE = 1000 * 1024 * 1024
        file_size = 0
        file_content = bytearray()
        
        while chunk := await file.read(1024 * 1024):
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=413,
                    detail="File size too large. Maximum size is 1000MB"
                )
            file_content.extend(chunk)

        print(f"Размер файла: {file_size} bytes")

        # Отправляем предварительный ответ
        print("Отправка предварительного ответа")
        response = JSONResponse(
            status_code=202,
            content={"message": "File accepted for processing"}
        )

        # Конвертация в base64
        file_string = base64.b64encode(file_content).decode('utf-8')
        print("Файл конвертирован в base64")

        try:
            print("Начало обработки файла")
            result: TranscriptionResult = await predictor.predict(
                file_string=file_string,
                group_segments=True,
                transcript_output_format="both",
                num_speakers=None,
                translate=False,
                language=None,
            )
            print("Файл успешно обработан")
            
            # Выводим результаты транскрипции в консоль
            print("Результаты транскрипции:")
            print(f"Язык: {result.language}")
            print(f"Количество спикеров: {result.num_speakers}")
            for segment in result.segments:
                print(f"Спикер: {segment.speaker}, Текст: {segment.text}, Начало: {segment.start}, Конец: {segment.end}")

        except Exception as e:
            print(f"Ошибка при обработке файла в predict: {str(e)}")
            raise

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

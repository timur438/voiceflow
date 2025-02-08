from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from predict import Predictor, Output
import tempfile
import os
import shutil
import json

app = FastAPI()

predictor = Predictor()
predictor.setup()

class TranscriptionRequest(BaseModel):
    group_segments: bool = True
    transcript_output_format: str = "both"
    num_speakers: int = None
    translate: bool = False
    language: str = None
    prompt: str = None
    summary_type: str = "summary"
    offset_seconds: int = 0

@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...), 
    request: str = Form(...),
):
    try:
        request_data = json.loads(request)
        transcription_request = TranscriptionRequest(**request_data)

        temp_file_path = await save_temp_file(file)

        result = await generate_status_messages(temp_file_path, transcription_request)

        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        return {"status": "success", "transcript": result['segments'], "summary": result.get('summary', "No summary available")}
    
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))


async def save_temp_file(file: UploadFile):
    try:
        temp_dir = "temp_files"
        os.makedirs(temp_dir, exist_ok=True)
        
        temp_file_path = os.path.join(temp_dir, file.filename)

        with open(temp_file_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)

        return temp_file_path

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving temporary file: {str(e)}")


async def generate_status_messages(file_path: str, request: TranscriptionRequest):
    try:
        result = predictor.predict(
            file=file_path,
            group_segments=request.group_segments,
            transcript_output_format=request.transcript_output_format,
            num_speakers=request.num_speakers,
            translate=request.translate,
            language=request.language,
            prompt=request.prompt,
            summary_type=request.summary_type,
            offset_seconds=request.offset_seconds,
        )

        return {
            "segments": result.segments,
            "summary": result.summary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
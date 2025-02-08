from fastapi import FastAPI, UploadFile, File, HTTPException, Response, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from predict import Predictor, Output
from summarizer import TranscriptSummarizer
import base64
import asyncio
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

        file_content = await file.read()

        result = await generate_status_messages(file_content, transcription_request)
        
        return {"status": "success", "transcript": result['segments'], "summary": result.get('summary', "No summary available")}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def generate_status_messages(file_content: bytes, request: TranscriptionRequest):
    try:
        file_string = base64.b64encode(file_content).decode("utf-8")
        
        result = predictor.predict(
            file_string=file_string,
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
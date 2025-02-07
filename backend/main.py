from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from .cog import Predictor, Output
import base64
import asyncio

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

async def generate_status_messages(file_content: bytes, request: TranscriptionRequest):
    try:
        yield "data: Starting transcription...\n\n"
        await asyncio.sleep(1)

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

        yield f"data: Transcription complete. Result: {result}\n\n"
    except Exception as e:
        yield f"data: Error occurred: {str(e)}\n\n"

@app.post("/transcribe")
async def transcribe(
    request: TranscriptionRequest,
    file: UploadFile = File(..., max_size=1000 * 1024 * 1024),  # 1000 МБ
):
    try:
        if file.size > 1000 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File size exceeds 1000 MB limit")

        file_content = await file.read()

        return StreamingResponse(
            generate_status_messages(file_content, request),
            media_type="text/event-stream",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

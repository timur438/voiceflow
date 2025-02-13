import base64
import bcrypt
import os
import uuid

from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Depends

from typing import List, Optional
from predict import Predictor, TranscriptionResult
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from dotenv import load_dotenv

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from database import SessionLocal, Account, Email, Transcript 
from utils import generate_encrypted_key, decrypt_key 

app = FastAPI()

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["voiceflow.ru"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = Predictor()
predictor.setup()

def send_email(to_email: str, link: str):
    try:
        sender_email = "3735@voiceflow.ru" 
        sender_password = os.getenv("SENDER_PASSWORD")
        smtp_server = "smtp.mail.selcloud.ru" 
        smtp_port = 1127

        subject = "Завершение регистрации"
        body = f"Пройдите по ссылке для завершения регистрации: {link}"
        
        # Создаем MIME сообщение
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password) 
            server.sendmail(sender_email, to_email, msg.as_string())
            print(f"Email sent to {to_email}")
    
    except Exception as e:
        print(f"Error sending email: {e}")

# Модели
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class CheckEmailRequest(BaseModel):
    email: EmailStr

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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def process_transcription(file_content: bytes):
    try:
        file_string = base64.b64encode(file_content).decode("utf-8")
        
        result: TranscriptionResult = await predictor.predict(
            file_string=file_string,
            num_speakers=None,
            translate=False,
            language=None,
        )
        
    except Exception as e:
        print(f"Ошибка обработки: {str(e)}")

@app.post("/check")
async def check_email(request: CheckEmailRequest, db: Session = Depends(get_db)):
    email = db.query(Email).filter(Email.email == request.email).first()
    if email:
        # Если email уже зарегистрирован, перенаправляем на страницу логина
        return RedirectResponse(url="/login?email=" + request.email)
    
    unique_token = str(uuid.uuid4()) 
    registration_link = f"https://voiceflow.ru/register?token={unique_token}"

    email_record = Email(email=request.email, token=unique_token)
    db.add(email_record)
    db.commit()
    
    send_email(request.email, registration_link)

    return {"message": "Check your email to complete registration"}

@app.post("/register")
async def register(token: str, request: RegisterRequest, db: Session = Depends(get_db)):
    email_record = db.query(Email).filter(Email.token == token).first()
    if not email_record:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    existing_email = db.query(Email).filter(Email.email == request.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    new_account = Account(username=request.email)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    encrypted_key = generate_encrypted_key(request.password)
    new_account.key = base64.b64encode(encrypted_key).decode('utf-8')

    # Удаляем токен после использования
    email_record.token = None
    db.commit()

    return {"message": "Registration successful"}

@app.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    email_record = db.query(Email).filter(Email.email == request.email).first()
    if not email_record:
        raise HTTPException(status_code=404, detail="Email not found")

    # Проверка пароля с использованием bcrypt
    stored_encrypted_key = email_record.account.key
    encrypted_data = base64.b64decode(stored_encrypted_key)
    
    # Расшифровка ключа с использованием функции из utils
    decrypted_key = decrypt_key(request.password, encrypted_data)
    
    return {"message": "Login successful", "decrypted_key": decrypted_key.hex()}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks(), decrypted_key: str = Depends(login), db: Session = Depends(get_db)):

    try:
        MAX_FILE_SIZE = 1000 * 1024 * 1024
        file_size = 0
        file_content = bytearray()
        
        while chunk := await file.read(1024 * 1024):
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                raise HTTPException(status_code=413, detail="File size too large. Maximum size is 1000MB")
            file_content.extend(chunk)
        
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
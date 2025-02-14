import base64
import bcrypt
import os
import uuid
import jwt
import logging
import subprocess
import hashlib
import hmac
from datetime import datetime, timedelta

from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Depends, Response, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from typing import List, Optional
from predict import Predictor, TranscriptionResult
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database import SessionLocal, Account, Email, Transcript 
from utils import generate_encrypted_key, decrypt_key 

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

SECRET_KEY = os.getenv("SENDER_PASSWORD")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 дней

app.add_middleware(
    CORSMiddleware,
    allow_origins=["voiceflow.ru"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = Predictor()
predictor.setup()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Декодируем токен
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

def generate_secure_token(email: str):
    timestamp = str(int(datetime.utcnow().timestamp()))
    data = f"{email}:{timestamp}"
    signature = hmac.new(SECRET_KEY.encode(), data.encode(), hashlib.sha256).hexdigest()
    return f"{data}:{signature}"

def verify_secure_token(token: str, email: str):
    try:
        parts = token.split(":")
        if len(parts) != 3:
            return False

        email_part, timestamp, signature = parts
        if email_part != email:
            return False

        expected_signature = hmac.new(SECRET_KEY.encode(), f"{email}:{timestamp}".encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_signature, signature):
            return False

        token_time = datetime.utcfromtimestamp(int(timestamp))
        if datetime.utcnow() - token_time > timedelta(hours=1):
            return False

        return True
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def send_email(to_email: str, link: str):
    try:
        sender_email = "no-reply@voiceflow.ru"
        subject = "Завершение регистрации"
        body = f"Пройдите по ссылке для завершения регистрации: {link}"
        
        command = f'echo "{body}" | mail -s "{subject}" {to_email}'
        
        subprocess.run(command, shell=True, check=True)
        print("Email sent successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error sending email: {e}")

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

class RegisterRequest(BaseModel):
    token: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class CheckEmailRequest(BaseModel):
    email: EmailStr

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        raise e
    finally:
        db.close()

@app.get("/validate-token")
async def validate_token(current_user: str = Depends(get_current_user)):
    return {"message": "Token is valid", "username": current_user}

@app.post("/check")
async def check_email(request: CheckEmailRequest, db: Session = Depends(get_db)):
    logger.info(f"Checking if email {request.email} already exists")
    
    existing_email = db.query(Email).filter(Email.email == request.email).first()
    
    if existing_email:
        account = db.query(Account).filter(Account.id == existing_email.account_id).first()
        
        if account:
            logger.info(f"Email {request.email} is already associated with an account, redirecting to /login")
            return RedirectResponse(url="/login?email=" + request.email)
        else:
            logger.info(f"Email {request.email} is not associated with any account, generating registration link")
            secure_token = generate_secure_token(request.email)
            registration_link = f"https://voiceflow.ru/register?token={secure_token}"

            existing_email.token = secure_token
            db.commit()
            
            send_email(request.email, registration_link)

            return {"message": "Check your email to complete registration"}
    
    logger.info(f"Email {request.email} not found, generating registration link")
    secure_token = generate_secure_token(request.email)
    registration_link = f"https://voiceflow.ru/register?token={secure_token}"

    email_record = Email(email=request.email, token=secure_token)
    db.add(email_record)
    db.commit()
    
    send_email(request.email, registration_link)

    return {"message": "Check your email to complete registration"}

@app.post("/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_email = db.query(Email).filter(Email.email == request.email).first()
    if not existing_email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    if not verify_secure_token(request.token, request.email):
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    existing_account = db.query(Account).filter(Account.email == request.email).first()
    if existing_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt()).decode()
    encrypted_key = generate_encrypted_key(request.password)
    
    new_account = Account(
        email=request.email,
        password_hash=hashed_password,
        encrypted_key=base64.b64encode(encrypted_key).decode('utf-8')
    )
    db.add(new_account)
    db.commit()
    
    access_token = create_access_token({"sub": request.email})
    decrypted_key = decrypt_key(request.password, encrypted_key).hex()
    
    return {"access_token": access_token, "key": decrypted_key, "email": request.email}

@app.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Account).filter(Account.email == request.email).first()
    if not user or not bcrypt.checkpw(request.password.encode(), user.password_hash.encode()):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    encrypted_data = base64.b64decode(user.encrypted_key)
    decrypted_key = decrypt_key(request.password, encrypted_data).hex()

    access_token = create_access_token({"sub": request.email})

    return {"access_token": access_token, "key": decrypted_key, "email": request.email}

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
    uvicorn.run(app, host="0.0.0.0", port=8080)
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, LargeBinary, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')
ssl_ca = os.getenv('DB_SSL_CA')
port = os.getenv('DB_PORT')

DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

Base = declarative_base()

engine = create_engine(DATABASE_URL, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    encrypted_key = Column(String(512))
    is_admin = Column(Boolean, default=False)
    emails = relationship("Email", back_populates="account", uselist=False)
    transcripts = relationship("Transcript", back_populates="account")

class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    token = Column(String(255), nullable=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship("Account", back_populates="emails")

class Transcript(Base):
    __tablename__ = 'transcripts'

    id = Column(Integer, primary_key=True, index=True)
    encrypted_data = Column(Text)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship("Account", back_populates="transcripts")

Base.metadata.create_all(bind=engine)
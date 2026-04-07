from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker
import random
import string
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"
    code = Column(String, primary_key=True)
    original_url = Column(String, nullable=False)
    click_count = Column(Integer, default=0)
    

Base.metadata.create_all(bind=engine)

app = FastAPI()

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class ShortenRequest(BaseModel):
    url: str

@app.post("/shorten")
def shorten_url(request: ShortenRequest):
    if not request.url.startswith("http://") and not request.url.startswith("https://"):
        raise HTTPException(status_code=400, detail="Invald URL format")
    session = SessionLocal()
    code = generate_code()
    new_url = URL(code=code, original_url=request.url)
    entry = session.query(URL).filter(URL.original_url == request.url).first()
    if entry != None:
        session.close()
        return {"short_code": entry.code}
    session.add(new_url)
    session.commit()
    session.close()
    return {"short_code": code}

@app.get("/{code}")
def redirect(code: str):
    session = SessionLocal()
    entry = session.query(URL).filter(URL.code == code).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="URL not found")
    try:
        entry.click_count += 1
        session.commit()
        return {"original_url": entry.original_url, "click_count": entry.click_count}
    finally:
        session.close()
    
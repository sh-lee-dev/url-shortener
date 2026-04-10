from fastapi import FastAPI, HTTPException, Depends
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

class ShortenResponse(BaseModel):
    short_code: str

@app.post("/shorten", response_model=ShortenResponse)
def shorten_url(request: ShortenRequest, db=Depends(get_db)):
    if not request.url.startswith("http://") and not request.url.startswith("https://"):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    code = generate_code()
    new_url = URL(code=code, original_url=request.url)
    entry = db.query(URL).filter(URL.original_url == request.url).first()
    if entry != None:
        return {"short_code": entry.code}
    db.add(new_url)
    db.commit()
    return {"short_code": code}

class RedirectResponse(BaseModel):
    original_url: str
    click_count: int

@app.get("/{code}", response_model=RedirectResponse)
def redirect(code: str, db=Depends(get_db)):
    entry = db.query(URL).filter(URL.code == code).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="URL not found")

    entry.click_count += 1
    db.commit()
    return {"original_url": entry.original_url, "click_count": entry.click_count}
    
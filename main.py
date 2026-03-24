from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.orm import sessionmaker
import random
import string
from pydantic import BaseModel

DATABASE_URL = "sqlite:///./urls.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"
    code = Column(String, primary_key=True)
    original_url = Column(String, nullable=False)

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
    session.close()
    if entry is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"original_url": entry.original_url}
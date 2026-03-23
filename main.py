from fastapi import FastAPI

app = FastAPI()

db = {}

@app.post("/shorten")
def shorten_url(url: str):
    code = str(len(db) + 1)
    db[code] = url
    return {"short_code": code}

@app.get("/{code}")
def redirect(code: str):
    return {"original_url": db.get(code, "not found")}
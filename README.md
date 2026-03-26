# URL Shortener

A simple URL shortening REST API built with FastAPI and SQLite.

## Live Demo URL
[Live Demo](https://url-shortener-production-de5e.up.railway.app/docs)

## Tech Stack
- FastAPI
- SQLite
- SQLAlchemy

## Run locally
pip install -r requirements.txt
uvivorn main:app reload

## Endpoints
- POST /shorten - shorten a URL
- GET /{code} - retrieve original URL
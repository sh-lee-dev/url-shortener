# URL Shortener

A REST API that shortens URLs, detects duplicates, and tracks click counts. Built with FastAPI and SQLite.

## Live Demo
[Live Demo](https://url-shortener-production-de5e.up.railway.app/docs)

## Architecture

```mermaid
flowchart TD
    Client([Client])

    Client -->|POST /shorten| Validation[Pydantic validation]
    Client -->|GET /{code}| Endpoint[Endpoints]
    Client -->|GET /stats/{code}| Stats[Stats endpoint]

    Validation --> DI
    Endpoint --> DI
    Stats --> DI

    subgraph FastAPI Application
        Validation
        Endpoint
        Stats
        DI[Dependency injection\nget_db]
        EH[Error handling\nHTTPException 400 / 404]
    end

    DI --> ORM[SQLAlchemy ORM]
    ORM --> DB[(SQLite\nurls.db)]
```

## Tech Stack
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- pytest

## Features
- Shorten URLs with a random 6-character code
- Duplicate URL detection — returns existing code if URL already exists
- Click count tracking per shortened URL
- HTTP error handling (400, 404)
- Deployed on Railway

## Endpoints
- `POST /shorten` — shorten a URL
- `GET /{code}` — retrieve original URL and increment click count
- `GET /stats/{code}` — retrieve click count only

## Run locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
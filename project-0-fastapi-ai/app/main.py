import logging

from fastapi import FastAPI, HTTPException

from app.config import settings
from app.schemas import (
    SummarizeRequest,
    SummarizeResponse,
    ClassifyRequest,
    ClassifyResponse,
    ExtractRequest,
    ExtractResponse,
)
from app.services.llm_service import LLMService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="A typed FastAPI API using Ollama + Mistral.",
)

service = LLMService()


@app.get("/")
def root():
    return {
        "message": "Typed Text Processing API is running.",
        "endpoints": ["/summarize", "/classify", "/extract", "/health"],
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "environment": settings.APP_ENV,
        "model": settings.OLLAMA_MODEL,
        "host": settings.OLLAMA_HOST,
    }


@app.post("/summarize", response_model=SummarizeResponse)
def summarize(payload: SummarizeRequest):
    try:
        return service.summarize(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Summarize endpoint failed: %s", exc)
        raise HTTPException(status_code=500, detail="Unexpected server error.") from exc


@app.post("/classify", response_model=ClassifyResponse)
def classify(payload: ClassifyRequest):
    try:
        return service.classify(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Classify endpoint failed: %s", exc)
        raise HTTPException(status_code=500, detail="Unexpected server error.") from exc


@app.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest):
    try:
        return service.extract(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Extract endpoint failed: %s", exc)
        raise HTTPException(status_code=500, detail="Unexpected server error.") from exc
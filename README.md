# Project 0 — Typed FastAPI AI API (Ollama + Mistral)

A beginner-friendly backend API built with **FastAPI**, **Pydantic**, and **Ollama + Mistral**.

This project provides three typed AI endpoints for:

* `/summarize` — summarize input text
* `/classify` — classify text into user-provided labels
* `/extract` — extract structured information from text

The goal of this project was to learn how to build a structured AI backend with proper request validation, response schemas, service-layer architecture, and local LLM integration.

---

## Features

* Typed FastAPI endpoints
* Request and response validation with Pydantic
* Local LLM integration using Ollama + Mistral
* JSON cleanup and schema validation for model outputs
* Clean project structure with separated route, schema, config, and service layers
* Easy testing with Postman or Swagger UI

---

## Tech Stack

* FastAPI
* Pydantic
* Ollama
* Mistral
* Uvicorn
* Python

---

## Project Structure

```text
project-0-fastapi-ai/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   └── services/
│       ├── __init__.py
│       └── llm_service.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## How It Works

1. A client sends a request to one of the API endpoints.
2. FastAPI validates the request body using Pydantic schemas.
3. The route function sends the validated input to the service layer.
4. The service layer builds prompts and sends them to Ollama.
5. Mistral returns raw text output.
6. The service layer cleans the output and attempts to extract valid JSON.
7. The JSON is validated against internal output schemas.
8. A final typed response is returned to the client.

---

## Local Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
ollama pull mistral
uvicorn app.main:app --reload
```

Server runs at:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

---

## Environment Variables

Create a `.env` file locally using this structure:

```env
APP_NAME=Typed Text Processing API
APP_ENV=development
OLLAMA_MODEL=mistral
OLLAMA_HOST=http://localhost:11434
```

Recommended `.env.example` for GitHub:

```env
APP_NAME=Typed Text Processing API
APP_ENV=development
OLLAMA_MODEL=mistral
OLLAMA_HOST=http://localhost:11434
```

---

## API Endpoints

### `GET /`

Returns a basic welcome response and the list of available endpoints.

### `GET /health`

Returns runtime health/config information such as environment, model, and Ollama host.

### `POST /summarize`

Summarizes input text.

Example request:

```json
{
  "text": "FastAPI is a modern Python framework for building APIs quickly and with automatic validation and documentation.",
  "max_words": 20
}
```

Example response shape:

```json
{
  "summary": "FastAPI is a Python framework for building APIs quickly with validation and documentation.",
  "original_word_count": 15,
  "summary_word_count": 12,
  "provider": "ollama",
  "model": "mistral"
}
```

### `POST /classify`

Classifies input text into one of the provided labels.

Example request:

```json
{
  "text": "I want a refund because my order arrived damaged.",
  "labels": ["billing", "refund", "technical support"]
}
```

Example response shape:

```json
{
  "label": "refund",
  "confidence": 0.92,
  "reasoning": "The user is asking for a refund due to a damaged order.",
  "provider": "ollama",
  "model": "mistral"
}
```

### `POST /extract`

Extracts requested structured fields from input text.

Example request:

```json
{
  "text": "Ali ordered a Dell laptop on March 2 for $700.",
  "fields": ["customer_name", "product", "date", "price"]
}
```

Example response shape:

```json
{
  "extracted_data": {
    "customer_name": "Ali",
    "product": "Dell laptop",
    "date": "March 2",
    "price": "$700"
  },
  "missing_fields": [],
  "provider": "ollama",
  "model": "mistral"
}
```

---

## Validation and Design Notes

* Input validation is handled with Pydantic request schemas.
* Output validation is handled with Pydantic response schemas.
* Extra unexpected fields are rejected using strict schema rules.
* Custom validators clean labels and extraction field inputs.
* LLM output is not trusted directly; it is cleaned and validated before returning it.

---

## What I Learned

Through this project, I learned:

* how FastAPI route handlers work
* how request and response validation works with Pydantic
* how to structure a backend project into separate layers
* how to connect a local LLM using Ollama
* how to clean and validate model-generated JSON
* how to test APIs using Postman and Swagger
* how to think in terms of input schemas, service logic, and typed outputs

---

## Challenges I Faced

Some of the practical issues I encountered while building this project included:

* Python import path and project structure issues
* Uvicorn module path confusion
* request body validation errors (`422`)
* understanding route-to-service flow
* forcing the model to return valid JSON consistently
* cleaning model output before parsing

---

## Limitations

This is a local-first project, which means:

* it depends on Ollama running locally
* it is not yet deployed as a cloud-hosted AI API
* it does not yet include authentication
* it does not yet include database integration
* it does not yet support streaming responses
* model output can still be imperfect and depends on prompt quality

---

## Future Improvements

Possible next upgrades:

* add authentication
* add structured logging improvements
* add streaming responses
* add database support
* add Docker support
* deploy with a hosted model backend
* add frontend interface
* improve prompt robustness and output reliability

---

## Why This Project Matters

This project is my foundation AI backend project.

It represents the starting point of my journey into AI application engineering, where I focused on understanding backend structure, typed APIs, schema validation, service-layer architecture, and local model integration before moving on to larger systems.

---

## Author Notes

This project was built as a learning-oriented portfolio piece. The goal was not just to make the endpoints work, but to understand how a structured AI backend is designed and how small backend systems can be extended into larger production-oriented projects later.

---



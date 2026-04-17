FROM python:3.10

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY project-0-fastapi-ai /code/project-0-fastapi-ai

WORKDIR /code/project-0-fastapi-ai

EXPOSE 8000

CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
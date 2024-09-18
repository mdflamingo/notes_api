FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-dev

RUN pip install --upgrade pip --no-cache-dir
RUN pip install poetry --no-cache-dir
ADD pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

CMD gunicorn main:app --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker
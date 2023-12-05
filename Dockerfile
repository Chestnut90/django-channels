FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.6.1

COPY pyproject.toml .

RUN pip install poetry==${POETRY_VERSION}
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

RUN mkdir /app/
WORKDIR /app/

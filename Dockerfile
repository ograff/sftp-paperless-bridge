# syntax=docker/dockerfile:1

FROM python:3.13-slim

ENV POETRY_VERSION=1.8.4 \
    POETRY_VIRTUALENVS_CREATE=false

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry install --no-interaction --no-ansi --no-root --no-dev

# Copy Python code to the Docker image
COPY sftp_paperless_bridge /code/sftp_paperless_bridge/

CMD ["poetry", "run", "sftp-paperless-bridge"]

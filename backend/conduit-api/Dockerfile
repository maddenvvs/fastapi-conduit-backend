FROM python:3.9-slim

WORKDIR /app
COPY ./shared/ ./shared/

WORKDIR /app/conduit-api
COPY ./conduit-api/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./conduit-api ./

EXPOSE 8080

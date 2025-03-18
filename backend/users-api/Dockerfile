FROM python:3.9-slim

WORKDIR /app
COPY ./shared/ ./shared/

WORKDIR /app/users-api
COPY ./users-api/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./users-api ./

EXPOSE 8080

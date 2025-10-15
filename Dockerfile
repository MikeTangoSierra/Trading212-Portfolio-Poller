# Use base image
FROM python:alpine3.18 AS base

ARG T212_API_TOKEN="1234adiadimai23923"
ARG T212_BASE_API_PATH="https://demo.trading212.com/api/v0/"
ARG MONGO_HOST="mongodb:27017"
ARG MONGO_PASSWORD=""
ARG MONGO_USER="mongo"
ARG RETAIN_DATA_FOR_DAYS=1000

ENV T212_API_TOKEN=$T212_API_TOKEN
ENV T212_BASE_API_PATH=$T212_BASE_API_PATH
ENV MONGO_HOST=$MONGO_HOST
ENV MONGO_PASSWORD=$MONGO_PASSWORD
ENV MONGO_USER=$MONGO_USER
ENV RETAIN_DATA_FOR_DAYS=$RETAIN_DATA_FOR_DAYS

WORKDIR /app

FROM base AS python_setup
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

FROM python_setup AS main
COPY src/ .
EXPOSE 5000
CMD ["python3", "-m", "flask", "--app", "main", "run", "--host=0.0.0.0"]
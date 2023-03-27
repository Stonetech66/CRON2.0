FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app/
ENV PYTHONUNBUFFERED=1
RUN chmod +x server.sh && chmod +x consumer.sh && chmod +x worker.sh




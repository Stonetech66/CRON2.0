FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip --no -cachedir install -r requirements.txt

COPY ./CRON2 /app/CRON2

CMD ["uvicorn", "CRON2.main:app", "--reload", "host ="] 
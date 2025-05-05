FROM python:latest

WORKDIR /app

COPY app/* .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "sh", "-c", "./run.sh" ]
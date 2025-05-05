FROM python:latest

WORKDIR /app

COPY app/* .

RUN pip install --upgrade pip

RUN python3 -m venv venv

RUN . venv/bin/activate

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "sh", "-c", "./run.sh" ]
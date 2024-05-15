FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY main.py main.py
COPY entrypoint.sh entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]

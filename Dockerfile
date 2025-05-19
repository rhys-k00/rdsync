# Dockerfile

FROM python:3.11-slim

WORKDIR /app
COPY sync.py .

RUN pip install requests

ENV RD_TOKEN=changeme
VOLUME /downloads

CMD ["python", "sync.py"]

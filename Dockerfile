FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFREAD 1

WORKDIR /usr/src/app

COPY ./app .

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libffi-dev \
    libnacl-dev \
    python3-dev \
    ffmpeg \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -U py-cord[voice] --pre --no-cache-dir
RUN pip install google-api-python-client youtube_dl --no-cache-dir

CMD ["python", "-u", "main.py"]

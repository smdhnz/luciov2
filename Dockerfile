FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFREAD 1

WORKDIR /usr/src/app

COPY ./app .

RUN apt install libffi-dev libnacl-dev python3-dev
RUN pip install -U py-cord[voice] --pre --no-cache-dir

CMD ["python", "-u", "main.py"]

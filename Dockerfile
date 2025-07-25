FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY req.txt /app/req.txt
RUN pip install --no-cache-dir -r req.txt

COPY . /app

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=adminpanel.settings

CMD ["python", "main.py"]

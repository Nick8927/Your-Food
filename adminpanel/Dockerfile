FROM python:3.11-slim

WORKDIR /app

COPY req_admin.txt .
RUN pip install --no-cache-dir -r req_admin.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

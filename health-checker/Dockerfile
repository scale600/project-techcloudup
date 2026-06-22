FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
ENV GCP_PROJECT=project-8ea04b35-82af-4a8d-845

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

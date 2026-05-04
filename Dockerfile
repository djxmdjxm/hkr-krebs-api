FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# --timeout 300: allow up to 5 minutes per request.
# Hamburg sends >100 MB XML per delivery; default 30s kills workers mid-upload
# on slower targets (Docker Desktop / WSL2 air-gap installs) and surfaces as
# "Netzwerkfehler beim Upload" in the browser (xhr.onerror).
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080", "--timeout", "300"]


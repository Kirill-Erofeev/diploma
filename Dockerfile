FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y espeak libespeak1 build-essential pkg-config speech-dispatcher scons git && \
    rm -rf /var/lib/apt/lists/* && \
    python -m pip install scons && \
    git clone --recursive https://github.com/RHVoice/RHVoice.git && \
    scons && \
    scons install && \
    rhvoice.vm -i vitaliy

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ls app/database/sql_app.db || echo "⚠️ WARNING: DB not found"

EXPOSE 8000

# CMD ["python", "app/main.py"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "./certs/key.pem", "--ssl-certfile", "./certs/cert.pem", "--reload"]
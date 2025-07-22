FROM python:3.11-slim
WORKD /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py

CMD ["python", "bot.py"]

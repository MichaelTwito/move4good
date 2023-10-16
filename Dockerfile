FROM python:3.11
WORKDIR /app
COPY app .
COPY scripts .
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt
WORKDIR /app

CMD ["python", "/app/main.py"]


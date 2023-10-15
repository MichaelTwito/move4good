FROM python:3.11
WORKDIR /app
ENV MYSQL_ROOT_PASSWORD="password"
ENV MYSQL_DATABASE="locator"
COPY app .
COPY scripts .
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt
WORKDIR /app

CMD ["python", "/app/app/main.py"]
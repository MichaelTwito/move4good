FROM python:3.11
WORKDIR /app
ENV MYSQL_ROOT_PASSWORD="password"
ENV MYSQL_DATABASE="locator"
COPY backend .
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt
WORKDIR /app

CMD ["create_user.py", "docker-user", "admin"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
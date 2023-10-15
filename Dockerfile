FROM python:3.11
WORKDIR /app
ENV MYSQL_ROOT_PASSWORD="password"
ENV MYSQL_DATABASE="locator"
COPY app .

COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt
WORKDIR /app
COPY scripts .

CMD ["chmod", "+x", "/app/scripts/init.sh"]

CMD ["./app/scripts/init.sh"]
CMD ["create_user.py", "admin", "admin","1"]

CMD ["python", "/app/app/main.py"]
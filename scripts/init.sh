#!/bin/sh

apk update && apk add mysql-client
# apk add bash
# Set the number of times to attempt pinging the server
MAX_ATTEMPTS=10

# Sleep interval in seconds between ping attempts
SLEEP_INTERVAL=5

# Function to check if MySQL server is alive
check_mysql_alive() {
  mysql -h $MYSQL_HOST -P 3306 -u $MYSQL_USER -p$MYSQL_ROOT_PASSWORD -e "CREATE DATABASE IF NOT EXISTS move_for_good;" &> /dev/null
  return $?
}

# Loop to check MySQL server availability
attempts=0
while [ $attempts -lt $MAX_ATTEMPTS ]; do
  if check_mysql_alive; then
    echo "MySQL server is alive."
    break
  else
    echo "MySQL server is not responding. Retrying in $SLEEP_INTERVAL seconds..."
    sleep $SLEEP_INTERVAL
    attempts=$((attempts + 1))
  fi
done

# If we reached here, it means MySQL server is still not alive after all attempts
if [ $attempts -eq $MAX_ATTEMPTS ]; then
  echo "MySQL server is not responding after $MAX_ATTEMPTS attempts. Exiting."
fi

pip install -r requirement.txt
python app/create_user.py admin admin 1
python app/main.py
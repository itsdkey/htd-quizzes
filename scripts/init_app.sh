#!/bin/bash

echo "stop htd apps and delete ALL named volumes..."
docker compose down --volumes

echo "start backend services..."
docker compose up -d app

echo "run migrations on new DB..."
docker exec -it backend-app bash -c "wait-for-it.sh db:5432 -- python manage.py migrate"

while true; do
  read -p "[optional] Do you want to prepopulate the DB? (y/n): " choice

  if [ "$choice" = "y" ]; then
    echo "prepopulate the DB..."
    docker exec -it backend-app bash -c \
      "wait-for-it.sh db:5432 --
      python manage.py init_quizzes"
    break
  elif [ "$choice" = "n" ]; then
    break
  else
    echo "Invalid choice. Please select y or n."
  fi
done

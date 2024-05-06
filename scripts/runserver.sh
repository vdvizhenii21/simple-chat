#!/bin/bash

# sh /scripts/init-crypto.sh;
#SCRIPT_PATH=$(realpath "$0")
#PARENT_PATH=$(dirname "$SCRIPT_PATH")  # Определяем родительскую директорию скрипта
#echo "The script is located at: $SCRIPT_PATH"
#ls -l "$PARENT_PATH"  # Выводим список файлов в родительской директории

if [ "$DEBUG" = "0" ]; then
  echo "Running in production mode...";
#   sh /scripts/migrate.sh;
#   sh /scripts/collectstatic.sh;
  gunicorn src.system.wsgi:application\
    -w $GUNICORN_WORKERS \
    --threads ${GUNICORN_THREADS:-1} \
    --bind :8081 \
    --max-requests=1000 \
    --worker-class=gthread \
    # --worker-class=gevent \
    --timeout=100 \
    --graceful-timeout=10\
    --log-level=DEBUG;
else
  echo "Running in development mode...";
  if [ "$USE_GUNICORN" = "1" ]; then
    gunicorn src.system.wsgi:application \
      -w $GUNICORN_WORKERS \
      --threads ${GUNICORN_THREADS:-1} \
      --bind :8081 \
      --reload  \
      --worker-class=gthread \
    #   --worker-class=gevent \
      --timeout=90 \
      --graceful-timeout=10\
      --log-level=DEBUG;
  else
    python /app/src/manage.py runserver 0.0.0.0:8081;
  fi
fi
# #!/bin/sh
# set -e
# if [ "$DATABASE" = "postgres" ]
# then
#     echo "Waiting for postgres..."

#     while ! nc -z $SQL_HOST $SQL_PORT; do
#       sleep 0.1
#     done

#     echo "PostgreSQL started"
# fi
echo "start entrypoint.sh"
python3 manage.py runserver
# python manage.py flush --no-input
# python manage.py migrate

# exec "$@"
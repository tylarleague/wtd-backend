#!/bin/sh
echo "Get inside virtual environment"
source env/bin/activate

echo "Install requirements"
pip install -r requirements.txt

echo "Install redis requirements"
pip install turfpy

echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database makemigrations"
python manage.py makemigrations


# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

#echo "Apply fixtures"
#python manage.py loaddata adding_superuser.json
#python manage.py loaddata initial_data.json

# Start server
echo "Starting server"
#python manage.py runserver 0.0.0.0:8000
gunicorn -b 0.0.0.0:8000 wtd.wsgi:application --log-level=info
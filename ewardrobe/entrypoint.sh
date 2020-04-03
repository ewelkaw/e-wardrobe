#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py runscript generate_data
python manage.py runscript load_data
python manage.py runserver 0.0.0.0:8000
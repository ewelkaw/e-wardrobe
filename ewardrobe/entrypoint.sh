#!/bin/sh

poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py runscript generate_data
poetry run python manage.py runscript load_data
poetry run python manage.py runserver 0.0.0.0:8000
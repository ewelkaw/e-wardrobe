FROM python:3.7-alpine3.10

RUN apk add --no-cache build-base libffi-dev openssl libressl-dev musl-dev postgresql-dev gcc python3-dev musl-dev bash
WORKDIR /app
ENV poetry=1.0.5
RUN pip3 install "poetry==$poetry"
COPY pyproject.toml poetry.lock ./
RUN poetry export --format=requirements.txt > requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 8000
COPY . /app
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
COPY ewardrobe/ewardrobe/secrets.docker.json /app/ewardrobe/ewardrobe/secrets.json
WORKDIR /app/ewardrobe
RUN python manage.py collectstatic
CMD gunicorn ewardrobe.wsgi --bind 0.0.0.0:$PORT
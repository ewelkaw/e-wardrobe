## App for online clothing shoping

1. Database
```bash
brew install postgresql
psql
```

2. Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Running server
```
python manage.py runserver
```

4. Loading data
```
python manage.py runscript load_data
```

5. Running tests
```
python manage.py test
```
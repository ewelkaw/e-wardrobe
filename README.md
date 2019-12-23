## App for online clothing shoping

1. Database
```bash
brew install postgresql
psql
```

Creating database:
```
CREATE DATABASE ewardrobe_db;

CREATE USER "user" WITH PASSWORD 'secret_password';

ALTER ROLE "user" SET client_encoding TO 'utf8';

ALTER ROLE "user" SET default_transaction_isolation TO 'read committed';

ALTER ROLE "user" SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE ewardrobe_db TO "user";
```

Exit postgres shell:
```
\q
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

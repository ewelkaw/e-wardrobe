## App for online clothing shoping

1. Database
```bash
brew install postgresql
psql
```

2. To use app in docker or locally there need to be two files added to:

```bash
~/little_ewardrobe/ewardrobe/ewardrobe/ $ touch secrets.docker.json
~/little_ewardrobe/ewardrobe/ewardrobe/ $ touch secrets.json
```
It should be filled according to:
```bash
~/little_ewardrobe/ewardrobe/ewardrobe/secrets.ci.json
```

2. Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Generating example data
```
python manage.py runscript generate_data
```
Data will be saved in `data` directory

4. Loading data from given csv
```
python manage.py runscript load_data
```

5. Running server

**locally:**
```
python manage.py runserver
```
**using docker:**
```
make build
make run 
```

**then in browser:**
```
http://localhost:8000/
```

6. Running tests

**locally:**
```
python manage.py test
```
**using docker:**
```

```

7. Running with admin panel
```
python manage.py createsuperuser
python manage.py runserver
go to: http://127.0.0.1:8000/admin/
```

8. Finite state machine in django

https://medium.com/@distillerytech/building-for-flexibility-using-finite-state-machines-in-django-2e36ddbd7708

`pip install django-fsm`
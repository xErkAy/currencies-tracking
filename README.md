# Sibdev

## Getting started

#### Copy the content from .env.example to .env file
```
cp .env.example .env
```

#### Then build containers with the following command

```
docker-compose up -d
```

#### Make and apply all the migrations.

```
python manage.py makemigrations project
python manage.py migrate project
python manage.py migrate
python manage.py makemigrations currency
python manage.py migrate
```

#### Create a superuser to use Django-Admin panel.

```
python manage.py createsuperuser
```
###

#### Then you have to fill up the database with currencies.

```
python manage.py fill_up_currencies
```

#### There is a script 'update_currencies_history.py' that runs every day at 12:00 pm. It has logs at /logs/update_currencies_history.log
#### But you can in run manually
```
python manage.py update_currencies_history
```
###

#### Now, you are ready to use the API.
The project uses nginx, so it runs on 80 port (wtih default settings).
```
http://localhost/api/
```
#### Notice: you have to be authenticated to use the API, so use the:
```
http://localhost/auth/registration/
```
#### to create a user.
####

#### Then use this to authenticate:
```
http://localhost/auth/
```

#### If you want to see the API docs, then use
```
http://localhost/docs/
```

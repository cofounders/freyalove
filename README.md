# freya love

## bootstrapping locally

1. create a virtualenv instance and activate it

2. run `pip install requirements`

3. configure your own `local_settings.py` with your local database information, template path etc.

4. you need to install PostgreSQL >= 8.4 on your local machine, create a database and a user role that will be used for this.

5. create a local_settings.py file to hold your local database configuration, project paths etc. an example:

	DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.

        'NAME': 'freyadb',                      # Or path to database file if using sqlite3.

        'USER': 'xyz',                      # Not used with sqlite3.

        'PASSWORD': '123123',                  # Not used with sqlite3.

        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.

	    'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.

	    }
	}

	FACEBOOK_ID = "1234567890"
	
	FACEBOOK_SECRET = "xxx1zCANdsafHAZasfsdfFREYALOVE"

6. run `python manage.py syncdb' # this tells Django to prep and setup the database

7. run `python manage.py migrate --all` # this tells Django to apply all the migrations and bring the database up to sync with the model definitions.

8. run `python manage.py runserver` # loads Django's dev server on port 8000, or alternatively you can hook it to your local instance of Gunicorn, Apache etc.

9. run `python manage.py loaddata` # loads the dummy data in

## libraries/dependencies overview

The Django app generally relies on [facebook-sdk][1] as the only third party library for the API, but there're a bunch of internal dependencies that you can see from `requirements.txt`.

## misc

1. please add *.pyc to your gitignore.

[1]: https://github.com/pythonforfacebook/facebook-sdk
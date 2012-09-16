# FreyaLove API

## pre-bootstrapping

1. You need to install [Python][2] (preferably 2.6+ but not version 3+ - why you say? Read [this][3].).
2. After you have Python instead, you need to download [virtualenv][4]

        tar zxvf virtualenv-x-x-x.tar.gz
        cd virtualenv-x-x-x
        python setup.py install


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

## server notes

To update any changes to the API, you need to simply restart Apache:

        sudo /etc/init.d/httpd restart

To load any fixtures manually,

        python manage.py loaddata <fixture name>

[1]: https://github.com/pythonforfacebook/facebook-sdk
[2]: http://www.python.org
[3]: http://stackoverflow.com/questions/4486589/should-i-learn-python-3-or-2-x/4486603#4486603
[4]: http://pypi.python.org/pypi/virtualenv/#downloads

## System Administration

### Automatically start services:

```
sudo /sbin/chkconfig httpd on
sudo /sbin/chkconfig nginx on
sudo /sbin/chkconfig postgresql on
```

### Manually restart all server processes:

```
sudo /etc/init.d/postgresql restart
sudo /etc/init.d/httpd restart
sudo /etc/init.d/nginx restart
```

### Poor Man's Continuous Integration

Set the cron jobs to run as as `root`.

```
sudo crontab -e
```

Update the client every 10 minutes. Update the API every 30 minutes.

```
*/10 * * * * cd /var/www/freyalove.com && git reset --hard && git pull origin master && cd www && h5bp && stylus styles/app.styl
*/30 * * * * cd /home/ec2-user/freyalove && git reset --hard && git pull origin master && /home/ec2-user/_env/bin/python manage.py migrate --all && /etc/init.d/httpd restart
```

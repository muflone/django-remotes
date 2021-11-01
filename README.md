# Django Remotes

**Description:** A Django application to execute remote commands 

**Copyright:** 2021 Fabio Castelli (Muflone) <muflone@muflone.com>

**License:** GPL-3+

**Source code:** https://github.com/muflone/django-remotes

**Documentation:** http://www.muflone.com/django-remotes/

# Description

Django remotes is a Django application to execute remote commands.

The project has a **Server** part to be installed in your network
in order to configure the enabled hosts and the commands to execute
for each group of host.

The other part is called **Client** which will need to be installed
in your client hosts, registered and then it will be able to receive
orders from the server side.

Containers or virtual environments usage is **highly encouraged** to
isolate from any other Python package installed in your system.

---

# Django Remotes server

To install the Django Remotes server you need to first install the
system requirements and then following the below installation
instructions.  

## System Requirements

The Python dependencies for the server part are listed in the
`requirements_server.txt` file.

* Python >= 3.9
* Django 3.2.x (https://pypi.org/project/Django/)
* Django Rest Framework 3.12.x (https://pypi.org/project/djangorestframework/)
* Cryptography 35.x (https://pypi.org/project/cryptography/)

Additional optional dependencies might be needed to use your desired
database.

## Settings file

You can setup your desired settings by editing the `project/settings.py`
file or by creating a new file into the `project` directory with the
following:

```python
from .settings import *

# Your_settings will go here
```

You can then specify the settings file using `--settings project.file`
flag or by setting the `DJANGO_SETTINGS_MODULE` environment variable.

```shell
export DJANGO_SETTINGS_MODULE=project.my_settings
```

## Database setup

You can use any database that is supported by Django and setup it
in a settings file.

For example to setup a SQLite database you can use the following:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/path/to/your-database.sqlite3',
    }
}
```

When you're ready with your database setup you can create all the
required tables and data using the following command:

```shell
python manage.py migrate
```

## Create a new Administrator account

Before you can start to use the application you need to create a new
administrator account using the following:

```shell
python manage.py createsuperuser
```

And following the instructions.

## Starting the server

The Django application should be served through a WSGI server like
gunicorn. For testing purposes only you can use the integrated Django
debug server.

To start the integrated Django debug server you can use:

```shell
python manage.py runserver 0.0.0.0:8000
```

This will start a server running on the TCP port 8000.

**Please remember to use the integrated Django debug server for
testing purposes only** as it's not a secure, fast and reliable
server to run Python applications.

## Usage

When you're ready open a web browser and navigate the page you set
during the server startup (eg http://localhost:8000/admin)

## Host registration token

In order to allow other clients to be registered you must pass them
a unique token generated during the database setup. This token can
be obtained using the following command:

```shell
python manage.py registration_token
```

---

# Django Remotes client

To install the Django Remotes server you need to first install the
system requirements and then following the below installation
instructions.  

## System Requirements

The Python dependencies for the server part are listed in the
`requirements_client.txt` file.

* Python >= 3.9
* Cryptography 35.x (https://pypi.org/project/cryptography/)
* Requests 2.x (https://pypi.org/project/requests/)

## Usage

The Django Remotes client usage first requires a host is registered
on a running Django Remotes server.

The registration can be done by command-line using the following:

```shell
python client.py \
  --action new_host \
  --url <SERVER URL> \
  --settings <SETTINGS FILE> \
  --token <HOST REGISTRATION TOKEN> \
  --private_key <PRIVATE KEY FILE PATH> \
  --public_key <PUBLIC KEY FILE PATH>
```

- `<SERVER URL>` argument must point to the server's root URL.
- `<SETTINGS FILE>` argument must be a file where to save the client
  settings.
- `<HOST REGISTRATION TOKEN>` argument must be obtained from the
  server using the `registration_token` command (see above).
- `<PRIVATE KEY FILE PATH>` argument must be a file path where to
  save the private key needed to encrypt the information between
  client and server. This file must be kept secret.
- `<PUBLIC KEY FILE PATH>` argument must be a file path where to
  save the public key needed to encrypt the information between
  client and server.

An example to register a new host is the following:

```shell
python client.py \
  --action new_host \
  --url http://192.168.1.50/ \
  --settings '/home/muflone/django-remotes/settings.ini' \
  --token 'ba1daf3e9d068e77a59cde64dffddcd6cd941f31' \
  --private_key '/home/muflone/django-remotes/key.pem' \
  --public_key '/home/muflone/django-remotes/key.pub'
```

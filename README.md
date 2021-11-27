# Django Remotes
[![Travis CI Build Status](https://img.shields.io/travis/com/muflone/django-remotes/master.svg)](https://www.travis-ci.com/github/muflone/django-remotes)
[![CircleCI Build Status](https://img.shields.io/circleci/project/github/muflone/django-remotes/master.svg)](https://circleci.com/gh/muflone/django-remotes)

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
in your client hosts and after being registered it will be able to
receive orders from the server side.

Containers or virtual environments' usage is **highly encouraged** to
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
* Django Admin List Filter Dropdown (https://pypi.org/project/django-admin-list-filter-dropdown/)
* Cryptography 35.x (https://pypi.org/project/cryptography/)

Additional optional dependencies might be needed to use your desired
database.

## Settings file

You can set up your desired settings by editing the `project/settings.py`
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

For example to set up a SQLite database you can use the following:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/path/to/your-database.sqlite3',
    },
    'api_logs': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/path/to/your-logs.sqlite3',
    }
}
```

When you're ready with your database setup you can create all the
required tables and data using the following command:

```shell
python manage.py migrate
python manage.py migrate --database api_logs
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
during the server startup (e.g. http://localhost:8000/admin)

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

After the registration you can test the registered host using:

```shell
python client.py \
  --action host_status \
  --settings <SETTINGS FILE>
```

If everything was set up properly you'll get a JSON response with
some information and hosts groups.

Now you're ready to get enabled awaiting commands to be executed
from the client using:

```shell
python client.py \
  --action commands_list \
  --settings <SETTINGS FILE>
```

If you get the following output:

```json
{
  "status": "OK",
  "results": []
}
```

Then you don't have any awaiting commands to execute else you'll
get a list of awaiting commands with their ID, for example:

```json
{
  "status": "OK",
  "results": [
    {
      "group": 1,
      "command": 2
    },
    {
      "group": 1,
      "command": 4
    }
  ]
}
```

From this example you have 3 commands to execute with the IDs 2 and 4.

You can execute a single command using the following syntax:

```shell
python client.py \
  --action command_get \
  --settings <SETTINGS FILE> \
  --command <COMMAND ID>
```

Executing the command you'll get a similar response:

```json
{
  "id": 1,
  "name": "<ENCRYPTED NAME>",
  "settings": {},
  "variables": {},
  "command": "<ENCRYPTED COMMAND>",
  "timeout": 15,
  "encrypted": [
    "name",
    "settings",
    "variables",
    "command"
  ],
  "encryption_key": "<ENCRYPTION KEY>",
  "stdout": "Platform: linux\n",
  "stderr": "[\n  \"linux\"\n]",
  "output": {
    "status": "OK",
    "results": {
      "id": 23
    }
  }
}
```

The first part contains the command details encrypted using an
encryption key.

The final part of the response will contain details about the last
executed command and with the data sent back to the server.

The command `commands_process` will execute every pending commands
prior terminating, you can use it to execute any command at once and
transmit all the responses to the server.

```shell
python client.py \
  --action commands_process \
  --settings <SETTINGS FILE>
```

The command `commands_monitor` will process every commands using the
previous command and then it will await for some seconds before
trying again to process every pending commands.

```shell
python client.py \
  --action commands_monitor \
  --settings <SETTINGS FILE> \
  --interval <SECONDS>
```

You can setup the server to await forever and listening for new
commands and process them when they become available to the client.

---

# Documentation and examples

Please refer to the `docs` directory for documentation and some usage
examples.

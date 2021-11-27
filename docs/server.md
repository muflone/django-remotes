# Django Remotes server setup

A simple approach to configure the server application is by running it
in a container like Docker.

Since the version 0.2.1 two files are shipped to ease the container
usage:
- `project/settings_container.py` will contain the default database
configuration
- `container-launch.sh` will execute all the database migration,
collect all the static files and will run the development server

**Warning**: for production environments you should avoid to use the
development server but switch a more robust WSGI server like gunicorn.

---

## Deployment using docker-compose

### Configure nginx

Create a `nginx.conf` to configure nginx to serve the web application
from a different port (8080) and to directly serve the static files
through nginx itself.

```
upstream backend {
  ip_hash;
  server backend:8080;
}

server {
  location /static/ {
    autoindex on;
    alias /static/;
  }

  location / {
    proxy_pass http://backend/;
  }
  listen 8000;
  server_name localhost;
}
```

### Create the containers stack

Create a new `docker-compose.yaml` file with the following:

```yaml
version: '3'

services:
  web:
    container_name: django-remotes_web
    image: nginx:1.21.3-alpine
    ports:
      - 8001:8000/tcp
    depends_on:
      - backend
    volumes:
      - ./static:/static
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./logs:/var/log/nginx

  backend:
    container_name: django-remotes_backend
    image: ilmuflone/django-remotes:0.2.1
    environment:
      - SERVER_PORT=8080
    expose:
      - 8080
    volumes:
      - ./static:/app/static
      - ./database.sqlite3:/var/lib/django-remotes.sqlite3
      - ./logs.sqlite3:/var/lib/django-remotes-logs.sqlite3
```

The directories `static` and `logs` can be initially empty, they will
be populated during the first container startup.

At the same way you could move your database outside of the container
by mapping the two files `django-remotes.sqlite` and
`django-remotes-logs.sqlite` thus those files can initially be empty
and they will be populated during the first startup.

Finally create the containers using the command `docker-compose up -d`

---

## Administrator configuration

With the container running you can create a new administrator account
using the command:

```shell
docker exec -it django-remotes_backend \
  python /app/manage.py createsuperuser \
  --settings project.settings_container
```

When asked fill the requested data to create a new administrator
account:

```
Username (leave blank to use 'root'): admin  
Email address: admin@localhost
Password: 
Password (again): 
Superuser created successfully.
```

---

## Server usage

You can now access to the server page http://localhost:8001/admin/

The port number 8001 was set in the docker-compose.yaml file.

---

## Server settings

In the `Settings` configuration section you can configure some
server setting.

- `server_url` - the server address used for the API request,
for example: `http://localhost:8001/`

- `hosts_group_auto_add` - a HostsGroup name to automatically add
the new hosts after the client registration

- `apilog_enable_logging` - a boolean value to enable or disable the
API requests logging (use 0 to disable, 1 to enable logging)

- `apilog_include_arguments` - a boolean value to include or exclude
the API requests arguments (its data) in the Api logs data

- `apilog_filter_users` - a list of comma separated user names to
exclude from the logging

---

## Registration token

To register new hosts you need to use a registration token which
will be automatically generated during the first start.

You can see or create the registration token again using the
`Tokens` section.

In the `Users` section you'll find two initial users:

- the administrator account created in the previous steps
- the `user_register_hosts` user which can be used to register new
hosts.

The `user_register_hosts` (or an alternative user) must be in the
`user_register_hosts` group (from the `Groups` section).

In the `Tokens` section you'll find the tokens created for the users
API requests, including the `user_register_hosts` user.

To find out the automatically created token for hosts registration
you can use the command: `python manage.py registration_token`.

In the case of a running container you can execute the command this
way:

```shell
docker exec -it django-remotes_backend \
  python /app/manage.py registration_token \
  --settings project.settings_container
```

---

## Client registration

For the client registration please refer to the README file with
the basic instructions.

```shell
python client.py \
  --action new_host \
  --url http://192.168.1.50/ \
  --settings '/home/muflone/django-remotes/settings.ini' \
  --token 'ba1daf3e9d068e77a59cde64dffddcd6cd941f31' \
  --private_key '/home/muflone/django-remotes/key.pem' \
  --public_key '/home/muflone/django-remotes/key.pub'
```

After a host registration some records will be automatically created:

- a new host in the `Hosts` section with the host public key used to
encrypt the data between the server and the client
- a new user in the `Users` section
- a new token in the `Tokens` section with the API token used to
authenticate during the requests

The new host will be automatically added to the `All hosts` Hosts
Groups, accordingly to the `hosts_group_auto_add` setting (see above).

From the `Hosts groups` section you can assign each host to any
group you prefer (Windows hosts, Linux hosts, client hosts).

---

## Host variables

You can configure many hosts variables that can be used to get
values from the hosts and save answers in the server application.

These values can be kept for internal reference (operating system,
system name, paths) or they can be passed to other commands to
apply some changes using the host data (imagine you first get the
host IP address and then reconfigure the host network using the
saved host IP address saved into a variable).

The variables can be created in the `Variables` section. Feel free
to assign any category to each variable and an unique name.

From the `Variable values` section you can review or assign new
values to each variable for each host. This configuration can be
made by hand or you can create a command and save a part of the
results into one or more variables.

---
## Commands configuration

You can finally configure the commands to run on each hosts group.

Each command must be assigned to a `Commands group` which defines
what hosts can access to the commands and the validity times for
each commands group.

After defining the commands groups you can define the commands to
be assigned to the group.

Each command can process any Python instruction and also print
some data which could be returned to the server.

Additionally each command can return one or more values in a  special
list variable called `__RESULT__`. Simply append each result to the
`__RESULT__` list.

Each command can receive one or more general settings values or one
or more host variables. This data will be passed to the command to
customize the command behavior using some general data or specific
host data.

---
## Commands results variables

The `__RESULT__` list from the commands can return one or more
data from the command to the server. This data can be saved into
one or more host variables.

The returned data from `__RESULT__` will be assigned to the host
variables using the defined order. The first result item will be
saved into the variables with order zero. Data with no variables
order matching will not be saved at all.

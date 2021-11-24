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

```
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

```
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

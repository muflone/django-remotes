# Django Remotes server deploy using Docker and Docker Compose

For a quick deploy you can use a docker container from Docker hub and build
the stack using `docker-compose` (or `docker compose` if you're using Docker
2.x).

## Files preparation

Before creating the stack make sure to prepare the following:

- a new empty directory named `static` that will be used to keep the static
files served directly from nginx. These files will be automatically collected
from Django remotes during the startup and made available to nginx.

- a new empty directory named `logs` used by nginx to save the log files

- a new file named `nginx.conf` with the configuration shown in the section

- a new empty file named `database.sqlite3` used as database for Django remotes
configuration tables

- a new empty file named `logs.sqlite3` used database for Django remotes logs

- a new file named `docker-compose.yaml` used to build the stack with
docker-compose (see below)

## Web server configuration

The `nginx.conf` file will enable nginx to serve the static files only from the
`/static` directory and pass everything else to Django remotes on the server
called `backend` on the port 8080.

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

## Docker compose configuration

This is the `docker-compose.yaml` file used to build the docker stack:

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

## Initialize the project

Create the containers stack using the command `docker-compose up -d` and wait
for the startup.

## Create the superuser account

With the container running you can create a new administrator account using the
following command:

```shell
docker exec -it django-remotes_backend \
  python /app/manage.py createsuperuser \
  --settings project.settings_container
```

When asked fill the requested fields like the example:

```
Username (leave blank to use 'root'): admin
Email address: <your email address>
Password: <your password>
Password (again): <your password>
Superuser created successfully.
```

## Access the Admin page

You can now access to the Admin page by opening the `http://<IP>:8001/admin`
page and use the credentials configured before.

## Server URL configuration

Before you continue on using the container you should set up the server URL
setting.

If you open the `http://<IP>:8001/api/status/` page you can see the following
result:

```json
{
  "status":"OK",
  "app_name":"Django Remotes",
  "version":"0.2.1",
  "server_url":"http://backend/",
  "discover":"/api/v1/discover/"
}
```

The `server_url` will show a different URL instead of the requested page.

This is due to the fact your server is running into a separated container whose
name is *backend*.

In the Server Administration page open the **Settings** section and configure
the `server_url` setting by changing its value to `http://<IP>:8001/`

When you load the status page again you'll get the fixed `server_url`:

```json
{
  "status":"OK",
  "app_name":"Django Remotes",
  "version":"0.2.1",
  "server_url":"http://<IP>:8001/",
  "discover":"/api/v1/discover/"
}
```

All the API requests will follow the `server_url` setting.

# Twenty-thirty backend

* [Env file](#env-file)
* [Backend devs](#backend-devs)
  * [Local development](#local-development-and-project-conventions)
* [Start the app project using docker-compose](#start-the-app-project-using-docker-compose)
* [Doing stuff related to the project](#doing-stuff-related-to-the-project)
  * [Always execute commands inside a container](#always-execute-commands-inside-a-container)
  * [Migrating and setting up database](#migrating-and-setting-up-database)
  * [Creating a superuser](#creating-a-superuser)
* [Prepopulate/recreate the DB](#prepopulaterecreate-the-db)
* [Testing](#testing)
* [Debugging](#debugging)



## Env file
Env variables are used around the project. To enable working on the project locally please copy the `.env-template`
file to the `.env` file:
```shell
cp .env-template .env
```


## Backend devs
### Local development and project conventions
You are going to push commits from your local computer.
In this project we have some conventions which are installed via pre-commit.
To use them you need to create a python virtual environment:
```shell
python3.12 -m venv env/
```

Activate the env and set PYTHONPATH:
```shell
source <path_to_env>/bin/activate
```

Install the pre-commit package and necessary hooks:
```shell
pre-commit install
```

Thanks to pre-commit each commit will be checked if it's in accordance with
project's conventions. More info here: https://pre-commit.com/


## Start the app project using docker-compose
This project contains the following containers:
- app - our backend API
- db - our Postgresql DB
- wdb - a python debugger for backend devs (more on that later)

To start the application and necessary containers locally with the following:
```shell
docker compose up app
```
Note: you can run this in the background just but adding the option `-d` so the command looks like:
`docker compose up -d`.

This will run all of necessary containers without the optional ones like `wdb`. To verify it is working please check
out the interactive API documentation at http://127.0.0.1:8000/openapi/swagger/


## Doing stuff related to the project
### Always execute commands inside a container
If you want to develop with docker compose you will need sometimes to execute commands
inside the app's container because the whole environment is there. This is a separate
environment from the one you have on your computer. Entering the container is also
necessary because all the env vars are loaded from the `.env` file, and they will help
you run your project smoothly.

All the commands below this paragraph will require you to enter the container first. To do that
please run one of the following commands:
```shell
docker compose run --rm app bash
```
or:
```shell
docker exec -it backend-app bash
```

The first one creates a separate container if you have the project already running
(it will be removed after exiting it). The second one will enter the running container
itself.

### Migrating and setting up database
If you want to modify database, start with changing the code in <django_app>/models.
Be sure that your app is in the setting's INSTALLED_APPS list. Then generate a migration
file with the following command:
```shell
python manage.py makemigrations <app_name>
```

Apply the migration with:
```shell
python manage.py migrate <app_name>
```

### Creating a superuser
This will create an Admin user for you. It will ask for the basic information it needs
to create an account. Use the following command:
```shell
python manage.py createsuperuser
```

### Prepopulate/recreate the DB
Sometimes it's helpful to have some existing data in your local DB. This can be useful
if you want to fool around the API our just test things manually. Here comes in handy
a simple script written specially for this kind of situation for you guys. It's called
"init_app.sh" and is located in the /scripts folder. To run it use the following:
```shell
bash scripts/init_app.sh
```

## Testing
Remember to be inside the container. Use the following command to execute all tests using the
Django's testrunner:
```shell
python manage.py test
```
Or you can run specific Apps/TestCases/tests by narrowing the command above:
```shell
python manage.py test <app_name>
python manage.py test <app_name>.tests.<class_name>
python manage.py test <app_name>.tests.<class_name>.<test_name>
```

# Debugging
You can debug your project using a debugger. When working with docker containers it's
easier to use a debugger called [WDB](https://github.com/Kozea/wdb). It allows to debug your workflow at runtime
using a web browser. The library is already installed, so you can use it right away.

**NOTE:** Just remember about setting the 3 necessary ENV vars in your `.env` file:
* PYTHONBREAKPOINT=wdb.set_trace
* WDB_NO_BROWSER_AUTO_OPEN=1
* WDB_SOCKET_SERVER=wdb

To use it, first, place a breakpoint somewhere in the code you want to investigate:
```python
breakpoint()
```
Then start the WDB container in the background:
```shell
docker compose up -d wdb
```

After these steps run your piece of code and check the statement inside the
[interactive console](http://127.0.0.1:1984/).

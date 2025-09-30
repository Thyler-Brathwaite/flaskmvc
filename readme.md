![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Flask MVC Template

A template for flask applications structured in the Model View Controller pattern [Demo](https://dcit-flaskmvc.herokuapp.com/). [Postman Collection](https://documenter.getpostman.com/view/583570/2s83zcTnEJ)

# Dependencies

- Python3/pip3
- Packages listed in requirements.txt

# Installing Dependencies

```bash
$ pip install -r requirements.txt
```

# Configuration Management

Configuration information such as the database url/port, credentials, API keys etc are to be supplied to the application. However, it is bad practice to stage production information in publicly visible repositories.
Instead, all config is provided by a config file or via [environment variables](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/).

## In Development

When running the project in a development environment (such as gitpod) the app is configured via default_config.py file in the App folder. By default, the config for development uses a sqlite database.

default_config.py

```python
SQLALCHEMY_DATABASE_URI = "sqlite:///temp-database.db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
```

These values would be imported and added to the app in load_config() function in config.py

config.py

```python
# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        delta = JWT_ACCESS_TOKEN_EXPIRES
...
```

## In Production

When deploying your application to production/staging you must pass
in configuration information via environment tab of your render project's dashboard.

![perms](./images/fig1.png)

# Flask Commands

`wsgi.py` is a utility script for performing various tasks related to the project. You can use it to import and test any code in the project.

## Database Initialization

```bash
$ flask init
```

Seeds the database with sample students, staff, accolades, and leaderboard.

## Student & Staff Commands

```bash
$ flask view-students     # view all students
$ flask view-staff        # view all staff members
$ flask view-logs         # view all service logs
```

## Service Log & Hours Commands

```bash
$ flask log-hours         # staff logs hours for a student
$ flask confirm-hours     # staff confirms a service log
$ flask request-confirm   # student requests confirmation for logged hours
```

## Leaderboard & Accolades

```bash
$ flask view-leaderboard  # view leaderboard rankings
$ flask view-accolade     # view student’s earned accolades
```

## User Management

User commands are grouped under `user`:

```bash
$ flask user create <username> <password>   # create a new user
$ flask user list [string|json]             # list all users
```

## Testing

Testing commands are grouped under `test`:

```bash
$ flask test user          # run all user-related tests
$ flask test user unit     # run only user unit tests
$ flask test user int      # run only user integration tests
$ pytest                   # run all application tests
```

# Running the Project

_For development run the serve command:_

```bash
$ flask run
```

_For production using gunicorn:_

```bash
$ gunicorn wsgi:app
```

# Deploying

You can deploy your version of this app to Render by clicking on the "Deploy to Render" link above.

# Database Migrations

If changes to the models are made, the database must be 'migrated' so that it can be synced with the new models.

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db --help
```

# Testing

## Unit & Integration

Unit and Integration tests are created in `App/test`. Commands are already provided in `wsgi.py`.

Example:

```bash
$ flask test user int
```

## Coverage

```bash
$ coverage report
$ coverage html
```

# Troubleshooting

## Views 404ing

If your newly created views are returning 404 ensure that they are added to the list in `main.py`.

## Cannot Update Workflow file

If you are running into errors in gitpod when updateding your github actions file, ensure your [github permissions](https://gitpod.io/integrations) in gitpod has workflow enabled ![perms](./images/gitperms.png)

## Database Issues

If you are adding models you may need to migrate the database. Alternatively you can delete your sqlite db file and reinitialize.

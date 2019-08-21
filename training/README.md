# Training documentation

## Getting started locally

### Prerequisites
- virtualenv or virtualenv wrapper
- pip
- PostgreSQL

### Step 1 - create and activate a virtualenv
This will depends on your installation, but make sure you create a virtualenv with python 3.6 or above as python interpreter

### Step 2 - install development requirements
Get inside project root folder and execute:
```bash
$ pip install -r requirements/local.txt
```

### Step 3 - create projects database
This step is up to you... good luck!

### Step 4 - Environment variables
At the root folder of your app create a new file called `.env` and add the following lines
```dotenv
# PostgreSQL
# ------------------------------------------------------------------------------
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=training
POSTGRES_USER=debug
POSTGRES_PASSWORD=debug
DATABASE_URL=postgres://debug:debug@localhost:5432/training
```
Adapt this file according to your setup and other needs

### Step 5 - apply migrations
```bash
$ pyhton manage.py migrate
```

### Step 6 - Load fixtures (optional)
```bash
$ python manage.py loaddata --app users admin
```
The above will create an admin user with username `admin` and password `training`

```bash
$ python manage.py loaddata --app core areas
```
The above will create all states and counties

### Step 7 - fire up your new app
```bash
$ python manage.py runserver 0.0.0.0:8000
```

## Models
![](models.png)
**Note:** Please make sure to update this diagram every time you make changes on models.
```bash
$ python manage.py graph_models -a -o models.png
```

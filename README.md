# Run Essenvia Task API

## Install Python

If you have not installed `python` already on your system, please follow [this link](https://www.python.org/downloads/) to install the same.

## Installing PostgreSQL

Please follow the steps mentioned [here](https://www.postgresql.org/download/) for your operating system to install `postgreSQL` in your system.

### Accesing `psql`

> If you are using linux as your driver OS you may follow the below steps. PostgreSQL usually create a user `postgres` who can access `psql`. So, we will try to access `psql` with user `postgres`.

```sh
sudo -su postgres psql
```

It will promt you to enter your root password. And after putting the right password you shall get access to `psql`.

### Creating Database

```sql
CREATE DATABASE essenvia;
```

### Creating Database User

```sql
CREATE USER essenvia WITH ENCRYPTED PASSWORD 'essenvia';
```

### Granting the database user `essenvia` access of the database `essenvia`

```sql
GRANT ALL PRIVILEGES ON DATABASE essenvia TO essenvia;
```

> Press `\q` followed by `enter` to come out of terminal

## Installing Redis

You may follow [these steps](https://redis.io/download) to install redis on your system. After installing it successfully, start the `redis-server`.

## Setting up the environment and environment variables

### Creating virtual environment

```sh
python -m venv env
```

This will create a virtual enironment with the name `env` in the project root.

### Activating the virtual environment

```sh
source env/bin/activate
```

You might see `(env)` in your terminal which states that the virtual environment is active. For example:

```sh
(env) kdpisda @ kuldeep-vostro ~/Projects/essenvia-task
```

### Installing the requirements

```sh
pip install -r requirements.txt
```

### Setting up the environment variables

If you changed anythig while we were preparing the database in `PostgreSQL` you might want to update the respective value in the `.env.temp` file. Rename the file to `.env`.

> Will now we have activated the virtual environment and have placed a `.env` file in the project root with the respective value. This step is required to run the server and the worker.

### Running the migrations

```sh
source .env && ./manage.py migrate
```

### Setting up admin username and password

```sh
source .env && ./manage.py createsuperuser
```

It will ask for `username`, `email`, `password` in a prompt, fill all the details and press enter. Make sure to enter email as well. So that we can login with the same credentials.

## Running Server

```sh
source .env && ./manage.py migrate
```

This will run the server in port `8000`

## Running Background Worker

Make sure you have activated the virtual environment. So in order for the better execution of the app we need to run the worker at the same time but in different terminal. So ideally, you would want to run the above command in one terminal, and the below command in the other terminal with virtual environment activated.

```sh
source .env && celery -A essenvia worker -l info
```

## Running React APP

In order to run the app, you must also have your [`React App Client`](https://github.com/kdpisda/essenvia-task-app) Clone the repository and follow the instructions specified in the `README.md` file in the [React App](https://github.com/kdpisda/essenvia-task-app) repository. Use the credentials defined while creating the admin user for the Django API.

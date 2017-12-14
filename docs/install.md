# Installation instructions

First create virtualenv in conda and activate it.

```
conda create -n timemanager python=3.5
```

Check if the env was created.

```
conda info --envs
```

Then activate the virtualenv.

```sh
source activate timemanager
# source deactivate
```

PS - To delete the environment, run

```sh
conda remove --name timemanager --all
```

-------

The next step is to install requirements. After making sure that you have activated the virtualenv, run the following command.

```sh
pip install -r requirements.txt
```

Then the next step is creating the database. We are using Postgres here.

```sql
create user tmadmin with password 'tmadmin';
create database timemanager with owner=tmadmin;
```

Now, we need to set the DATABASE_URL to environment.

```sh
export DATABASE_URL=postgresql://tmadmin:tmadmin@localhost:5432/timemanager
```

-----

The next steps are for actually running the application.

To run the application, use -

```sh
python manage.py runserver
```

Occassionally, you might need to do database upgrades as well (when database changes). For that use the following comamnds.

```sh
python manage.py db migrate
python manage.py db upgrade
```

*[dev]* For resolving migrations conflicts, use the following commands.

```sh
python manage.py db heads
python manage.py db merge HEAD1 HEAD2
python manage.py upgrade
```


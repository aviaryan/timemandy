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

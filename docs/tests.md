# Testing


First, create the test database.

```sql
create user tmadmin with password 'tmadmin';
create database timemanager_test with owner=tmadmin;
```

Then run the tests

```sh
python -m unittest discover tests/
```

# Django Atomic Migrations

[![Build Status](https://drone.srv.kojedz.in/api/badges/krichy/django-atomic-migrations/status.svg)](https://drone.srv.kojedz.in/krichy/django-atomic-migrations)

This small package ensures that Django's migration tracking model has an
unique index for applied migrations, and also ensures that migrations
steps are applied in transactions. This is known to work with
PostgreSQL.

## Usage

Install the package:
```bash
$ pip install django-atomic-migrations
```
Then, add the application to `INSTALLED_APPS` in your Django project:
```
INSTALLED_APPS = [
	...
	'django_atomic_migrations.AtomicMigrations',
	...
]
```

If your project's database already exists, you should run
```bash
$ python manage.py add-migrations-constraint
```
to create the missing unique constraint.

# Django Atomic Migrations

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

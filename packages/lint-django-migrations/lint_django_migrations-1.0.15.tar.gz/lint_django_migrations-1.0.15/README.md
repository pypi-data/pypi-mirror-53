# Lint Django migrations

## Install
```bash
pip install lint_django_migrations
```

## How to use
1. Install the app in settings.py
```python
INSTALLED_APPS = [
    # ...
    "lint_django_migrations",
]
```

2. Check your migrations
```bash
python manage.py lintmigrations
```
This will return an error if any of the migrations are backwards incompatible.

3. Fix errors
If there is an error, you have 2 options. Fix the migration or tell the linter that
the migration is not backwards incompatible. If you feel the migration is ok, run the command
again with the `--interactive` flag
```bash
python manage.py lintmigrations --interactive
```

## Setup on existing code base
If you would like to setup the linter on the existing codebase, it can be tedious to mark
every applied migration as valid. For that purpose, you can snapshot the current state and
just run the linter on future migrations
```bash
python manage.py lintmigrations --force-update

## All API options

```

## Run the linter in CI
If you want to run the linter, but not update the state use the following command
```bash
python manage.py lintmigrations --check-only
```

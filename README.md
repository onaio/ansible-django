# ansible-django #

[![Build Status](http://cicd.onalabs.org/api/badges/onaio/ansible-django/status.svg)](http://cicd.onalabs.org/onaio/ansible-django)

Use this role to install, configure, and manage [Django](https://www.djangoproject.com/).

This is a very simple and purist role for django installation.  We only install and configure:

- Django
- Celery (optional)

We intentionally consider the installation and configuration of databases, web servers, and other things as out of scope for this role.  Therefore, naturally this role is to be used in a playbook that installs and configures those other things.

Both `Django` and `celery` are installed and set up as `systemd` services.

## Role Variables ##

Some of the more important variables are briefly described below.  You can see all variables by looking at the `defaults/main.yml` file.

```yml
system_user: "django_app"  # name of the user that will own the django installation

python_source_version: "3.6"  # the python verion to user
python_version: "python3.6"  # the python version to use with pip commands

git_url: "https://github.com/moshthepitt/django-template3.git"  # the git repo of your django app which we are installing

local_settings_path: "path to /local_settings.py"  # Path to the Django settings file
django_settings_module: "template3.settings"  # Django settings module
wsgi_module: "template3.wsgi:application"  # Django wsgi module
```

You can look at `tests/test.yml` for examples of how to use these variables.

### Django Settings ###

You can set any and all Django settings using the `django_settings` variable.

Here is a fairly simple example:

```yml
django_settings:
  BASE_DIR: "os.path.dirname(os.path.dirname(__file__))"
  SITE_ID: 1
  STATIC_ROOT: "'/var/www/static'"
  STATIC_URL: "'/static/'"
  MEDIA_ROOT: "'/var/www/media'"
  MEDIA_URL: "'/media/'"
  EMAIL_BACKEND: "'django.core.mail.backends.console.EmailBackend'"
  EMAIL_HOST: "'localhost'"
  EMAIL_PORT: "1025"
  DEFAULT_FROM_EMAIL: "'Hello World <hello@example.com>'"
  ALLOWED_HOSTS: "[]"
  DEBUG: True
```

As you may have noticed the `django_settings` takes `key: value` arguments of the Django settings variables that we know and love.

For example, to set Debug=True, you would do:

```yml
django_settings:
  DEBUG: True
```

To set up your database, you'd do:

```yml
django_settings:
  DATABASES: |
    {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': 'somedb',
          'USER': 'someuser',
          'PASSWORD': 'hunter2',
          'HOST': '127.0.0.1',
          'PORT': '5432',
      }
    }
```

## Role Dependencies ##

* ANXS.python

You can install these by running the following ansible command:

```sh
ansible-galaxy install -r requirements.yml
```

## Testing ##

This project comes with a Vagrantfile, this is a fast and easy way to test changes to the role, fire it up with `vagrant up`.

See [vagrant docs](https://docs.vagrantup.com/v2/) for getting setup with vagrant

## License ##

Apache 2

## Authors ##

[Ona Engineering](https://ona.io)

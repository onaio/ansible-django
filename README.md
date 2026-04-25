# ansible-django

[![Build Status](https://github.com/onaio/ansible-django/workflows/CI/badge.svg)](https://github.com/onaio/ansible-django/actions?query=workflow%3ACI)

Use this role to install, configure, and manage [Django](https://www.djangoproject.com/).

This is a very simple and purist role for django installation. We only install and configure:

- Django
- Celery (optional)

We intentionally consider the installation and configuration of databases, web servers, and other things as out of scope for this role. Therefore, naturally this role is to be used in a playbook that installs and configures those other things.

Both `Django` and `celery` are installed and set up as `systemd` services.

## Role Variables

Some of the more important variables are briefly described below. You can see all variables by looking at the `defaults/main.yml` file.

```yml
django_system_user: "django_app" # name of the user that will own the django installation

django_python_apt_ppa: "ppa:deadsnakes/ppa" # The repository used to install python
django_python_version: "python3.8" # the python version to use with pip commands
django_python_packages: # the python packages that would be required
  - "{{ django_python_version }}"
  - "{{ django_python_version }}-dev"
  - python3-pip
  - python3-setuptools
django_pip_executable: "pip3" # Executable to use when running pip commands

django_git_url: "https://github.com/moshthepitt/django-template3.git" # the git repo of your django app which we are installing

django_local_settings_path: "path to /local_settings.py" # Path to the Django settings file
django_settings_module: "template3.settings" # Django settings module
django_wsgi_module: "template3.wsgi:application" # Django wsgi module
```

You can look at `tests/test.yml` for examples of how to use these variables.

### Django Settings

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

## uv (Astral) install mode

The role can install Python dependencies via [uv](https://docs.astral.sh/uv/) instead of pip, pipenv, or poetry. This mode requires the consuming project to have a `pyproject.toml` and `uv.lock` checked in.

Enable it by setting:

```yml
django_use_uv: true
django_use_regular_old_pip: false
django_use_pipenv: false
django_use_poetry: false
```

When enabled, the role:

1. Installs the `uv` binary to `/usr/local/bin/uv` on the host (idempotent — re-runs are no-ops).
2. Runs `uv sync --frozen --no-dev --python {{ django_python_version }}` against `{{ django_uv_project_dir }}` (defaults to `{{ django_checkout_path }}`), with `UV_PROJECT_ENVIRONMENT={{ django_venv_path }}` so the resulting venv lands at the path the rest of the role (uwsgi, systemd units) expects.
3. Continues to install `django_pip_packages` (uwsgi, celery, etc.) into the same venv via the role's existing pip step — no change there.

Tunables:

| Variable | Default | Purpose |
|---|---|---|
| `django_use_uv` | `false` | Enable the uv install mode. |
| `django_uv_version` | `"latest"` | Version installed via the astral.sh installer. Pin to e.g. `"0.6.10"` for reproducibility. |
| `django_uv_project_dir` | `"{{ django_checkout_path }}"` | Directory containing `pyproject.toml` + `uv.lock`. |
| `django_uv_sync_args` | `"--frozen --no-dev"` | Flags passed to `uv sync`. |

## Testing

This project utilizes molecule for testing, the molecule tool can be installed by running `pip install 'molecule[docker]'` after which tests can run with `molecule test --all`

This project also comes with a Vagrantfile, which is a fast and easy alternative to test changes to the role, fire it up with `vagrant up`. _See [vagrant docs](https://docs.vagrantup.com/v2/) for getting setup with vagrant_

## License

Apache 2

## Authors

[Ona Engineering](https://ona.io)

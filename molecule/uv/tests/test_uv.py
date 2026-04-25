import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_uv_binary_installed(host):
    uv = host.file('/usr/local/bin/uv')
    assert uv.exists
    assert uv.mode & 0o111  # executable

    cmd = host.run('/usr/local/bin/uv --version')
    assert cmd.rc == 0
    assert 'uv' in cmd.stdout


def test_venv_python_present(host):
    venv_python = host.file(
        '/home/sample_uv_app/.virtualenvs/sample_uv_app/bin/python'
    )
    assert venv_python.exists


def test_django_admin_in_venv(host):
    django_admin = host.file(
        '/home/sample_uv_app/.virtualenvs/sample_uv_app/bin/django-admin'
    )
    assert django_admin.exists
    assert django_admin.mode & 0o111


def test_extras_pip_packages_installed_into_uv_venv(host):
    # The role's mode-agnostic extras-pip step (django_pip_packages) must
    # install into the same venv uv created. tally-ho relies on this for
    # uwsgi; the converge sets django_pip_packages to ["click"].
    pip_show = host.run(
        '/home/sample_uv_app/.virtualenvs/sample_uv_app/bin/python '
        '-m pip show click'
    )
    assert pip_show.rc == 0
    assert 'Name: click' in pip_show.stdout

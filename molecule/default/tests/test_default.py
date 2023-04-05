import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'

def test_django_service(host):
    django_app = host.service("django_example_app")
    assert django_app.is_running
    assert django_app.is_enabled

    celeryd_django_app = host.service("celeryd-django_example_app")
    assert celeryd_django_app.is_running
    assert celeryd_django_app.is_enabled

    celerybeat_django_app = host.service("celerybeat-django_example_app")
    assert celeryd_django_app.is_running
    assert celeryd_django_app.is_enabled

def test_django_wsgi_file(host):
    content = host.file('/home/django_example_app/app/uwsgi.ini').content_string
    assert "env=SOME_ENV=Some value" in content

def test_uwsgi_config(host):
    uwsgi_settings = host.file("/home/django_example_app/app/uwsgi.ini")
    assert uwsgi_settings.contains("ignore-sigpipe = true")

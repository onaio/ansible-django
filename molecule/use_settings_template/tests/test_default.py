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

def test_local_setting_template(host):
    local_settings = host.file("/home/django_example_app/app/kaznet/settings/local_settings.py")
    assert local_settings.contains('MEDIA_ROOT = "/var/www/media/"')
    assert local_settings.user == "django_example_app"
    assert local_settings.group == "www-data"
    assert local_settings.mode == 0644
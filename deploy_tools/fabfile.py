from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, get
import random
import time
import io


REPO_URL = 'https://github.com/christianwaldmann/starting-page.git'
USERNAME = 'meinuser'


"""
Tools for deployment

Functions:
- setup_server()
- deploy()
- backup_database()

Requirements:
- blank ubuntu 20.04
- non root user is set up and is the same as USERNAME above here
"""


def deploy():
    """
    Deploy django and react project to ubuntu server.
    """
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    frontend_folder = source_folder + '/frontend'
    _create_directory_structure_if_necessary(site_folder)
    print(f"Fetching latest source from {REPO_URL}")
    _get_latest_source(source_folder)
    print("Making changes in settings.py for deployment")
    _update_settings(source_folder, env.host)
    print("Updating virtualenv")
    _update_virtualenv(source_folder)
    print("Updating npm dependencies")
    _update_npm_dependencies(source_folder)
    print("Updating static files")
    _update_static_files(source_folder)
    print("Updating databse")
    _update_database(source_folder)
    print("Making changes in frontend for deployment")
    _update_frontend(frontend_folder, env.host)
    print("Creating new build for frontend")
    _build_frontend(frontend_folder)
    print("Restarting services (gunicorn and nginx) or creating them if not exists")
    _restart_services_or_create_if_not_exists(source_folder, env.host)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/backend/api/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, 'ALLOWED_HOSTS = .+$',
        f'ALLOWED_HOSTS = ["{site_name}"]')

    secret_key_file = source_folder + '/backend/api/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/backend/requirements.txt')


def _update_static_files(source_folder):
    run(f'cd {source_folder}/backend && ../../virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database(source_folder):
    run(f'cd {source_folder}/backend && ../../virtualenv/bin/python manage.py migrate --noinput')


def _update_npm_dependencies(source_folder):
    run(f'cd {source_folder}/frontend && npm install')


def _update_frontend(frontend_folder, sitename):
    indexjs_path = frontend_folder + "/src/index.js"
    sed(indexjs_path, 'axios.defaults.baseURL = .+$',
        f'axios.defaults.baseURL = "https://{sitename}/api";')


def _build_frontend(frontend_folder):
    run(f'cd {frontend_folder} && npm run build')


def _restart_services_or_create_if_not_exists(source_folder, sitename):
    if not _gunicorn_systemd_service_exists(sitename):
        _setup_gunicorn_systemd_service(source_folder, sitename)
    else:
        _restart_gunicorn_systemd_service(sitename)
    if not _nginx_configuration_exists(sitename):
        _setup_nginx_configuration(source_folder, sitename)
    else:
        _restart_nginx_configuration()


def _gunicorn_systemd_service_exists(sitename):
    return exists(f'/etc/systemd/system/gunicorn-{sitename}.service')


def _setup_gunicorn_systemd_service(source_folder, sitename):
    run(f'cd {source_folder} && sed "s/SITENAME/{sitename}/g; s/USERNAME/{USERNAME}/g" deploy_tools/gunicorn-systemd.template.service | sudo tee /etc/systemd/system/gunicorn-{sitename}.service')
    run('sudo systemctl daemon-reload')
    run(f'sudo systemctl enable gunicorn-{sitename}')
    run(f'sudo systemctl start gunicorn-{sitename}')


def _restart_gunicorn_systemd_service(sitename):
    run(f"sudo systemctl restart gunicorn-{sitename}")


def _nginx_configuration_exists(sitename):
    return exists(f'/etc/nginx/sites-available/{sitename}')


def _setup_nginx_configuration(source_folder, sitename):
    run(f'cd {source_folder} && sed "s/SITENAME/{sitename}/g; s/USERNAME/{USERNAME}/g" deploy_tools/nginx.template.conf | sudo tee /etc/nginx/sites-available/{sitename}')
    run(
        f'sudo ln -s /etc/nginx/sites-available/{sitename} /etc/nginx/sites-enabled/{sitename}')
    run('sudo systemctl daemon-reload')
    run(f'sudo systemctl reload nginx')


def _restart_nginx_configuration():
    run('sudo systemctl reload nginx')


def backup_database():
    """
    Backup sqlite3 database on server aswell as local machine.
    """
    site_folder = f'/home/{env.user}/sites/{env.host}'
    current_time_in_unix = int(time.time())
    DB_NAME = f"db.{current_time_in_unix}.sqlite3"
    run(f"mkdir -p {site_folder}/backups")
    print("Backing up database on server")
    run(
        f'cp {site_folder}/database/db.sqlite3 {site_folder}/backups/{DB_NAME}')
    print('Backing up database on local machine')
    get(f"{site_folder}/backups/{DB_NAME}", f"../../backups/{DB_NAME}")


def setup_server():
    # def setup_server(DJANGO_SECRET_KEY):
    """
    Setup a blank server to be ready for deployment
    """
    # if not DJANGO_SECRET_KEY:
    #     raise Exception(
    #         "Error: No value set for DJANGO_SECRET_KEY, argument required.")
    print("Setting up server")
    print("Updating apt source")
    _update_apt_source()
    print("Upgrading apt packages")
    _upgrade_apt_packages()
    print("Installing apt packages")
    _install_apt_packages()
    print("Installing virtualenv")
    _install_virtualenv()
    # print("Setting system environment variables")
    # _set_system_environment_variables(DJANGO_SECRET_KEY)
    print("Starting nginx")
    _start_nginx()
    print("Done setting up server")


def _update_apt_source():
    run("sudo apt-get -qq update")


def _upgrade_apt_packages():
    run("sudo apt-get -qq upgrade")


def _install_apt_packages():
    run("sudo apt-get -qq install vim python3-pip python3-venv nginx python3.7 git npm")


def _install_virtualenv():
    run("pip3 install virtualenv")


def _set_system_environment_variables(secret_key):
    secret_key_on_server = _read_file('/etc/environment')
    if secret_key != secret_key_on_server:
        run(f'echo "DJANGO_SECRET_KEY={secret_key}" >> /etc/environment')


def _read_file(file_path, encoding='utf-8'):
    io_obj = io.BytesIO()
    get(file_path, io_obj)
    return io_obj.getvalue().decode(encoding)


def _start_nginx():
    run('systemctl start nginx')

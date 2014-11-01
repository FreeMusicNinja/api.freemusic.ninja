from fabric.api import *  # noqa


env.hosts = [
    '104.131.30.135',
]
env.user = "root"
env.directory = "/home/django/api.freemusic.ninja"
env.deploy_path = "/home/django/django_project"


def deploy():
    with cd(env.directory):
        run("git reset --hard origin/master")
        sudo("pip3 install -r requirements.txt")
        sudo("python3 manage.py collectstatic --noinput", user='django')
        sudo("python3 manage.py migrate --noinput", user='django')
        run("rm -f {deploy_path}".format(deploy_path=env.deploy_path))
        run("ln -s {project_path} {deploy_path}".format(
            project_path=env.directory, deploy_path=env.deploy_path))
        run("service gunicorn restart")


def dbshell():
    with cd(env.directory):
        sudo("python3 manage.py dbshell", user='django')


def shell():
    with cd(env.directory):
        sudo("python3 manage.py shell", user='django')


def migrate():
    with cd(env.directory):
        sudo("python3 manage.py migrate", user='django')


def gunicorn_restart():
    run("service gunicorn restart")

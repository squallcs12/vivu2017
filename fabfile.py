import datetime

from fabric.api import run, local, put
from fabric.contrib.files import append

now = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')

PYTHON_DIR = '/home/www/python'
CURRENT_DIR = '%s/current' % PYTHON_DIR
BUILDS_DIR = '%s/builds' % PYTHON_DIR
DEPLOY_DIR = '%s/%s' % (BUILDS_DIR, now)
SHARED_DIR = '%s/shared' % PYTHON_DIR
ENV_FILE = '%s/env' % SHARED_DIR
RUN_DIR = '%s/run' % SHARED_DIR
STATIC_DIR = '%s/static' % SHARED_DIR
LOG_DIR = '%s/log' % SHARED_DIR
MEDIA_DIR = '%s/media' % SHARED_DIR

PYTHON_LIBS = ('tk-dev libreadline-dev libssh-dev libsqlite3-dev libbz2-dev libncurses5-dev liblzma-dev '
               'libgdbm-dev libffi-dev')


def mkdirs():
    """Make base folders for deployment"""
    dirs = [
        PYTHON_DIR,
        BUILDS_DIR,
        SHARED_DIR,
        RUN_DIR,
        STATIC_DIR,
        LOG_DIR,
        MEDIA_DIR,
    ]
    for dir in dirs:
        _run_web("mkdir -p %s" % dir)
    _run_web("touch %s" % CURRENT_DIR)


def django(command):
    _run_env('cd {}; python manage.py {}'.format(CURRENT_DIR, command))


def restart_web():
    """Restart web services"""
    run("supervisorctl -c {}/server/supervisor.conf restart all".format(CURRENT_DIR))
    run('service nginx restart')


def setenv(name, value):
    """Set environment variable"""
    append(ENV_FILE, '{}=\'{}\''.format(name, value))
    restart_web()


def deploy():
    """Deploy current HEAD to server"""
    _clone_code()
    _install_requirements()
    _migrate()
    _collect_static()
    _make_link()
    _restart_supervisor()
    _restart_nginx()


def _run_web(command):
    return run("su www -c '%s'" % command.replace("'", "\\'"))


def _run_env(command):
    _run_web('source /usr/share/virtualenvwrapper/virtualenvwrapper.sh; workon env; {}'.format(command))


def _link_shared(source, to):
    _run_web('cd {}; ln -sn {} {}'.format(DEPLOY_DIR, source, to))


def _clone_code():
    local('git archive HEAD --prefix="{}/" -o deploy.tar'.format(now))
    put('deploy.tar', BUILDS_DIR, mode=777)

    deploy_file = '{}/deploy.tar'.format(BUILDS_DIR)
    run('chmod 0777 {}'.format(deploy_file))
    _run_web('cd {}; tar -xf deploy.tar'.format(BUILDS_DIR))

    run('rm {}'.format(deploy_file))

    _link_shared(ENV_FILE, './.env')
    _link_shared(STATIC_DIR, './static')
    _link_shared(MEDIA_DIR, './media')

    local('rm deploy.tar')


def _install_requirements():
    _run_env('cd {}; pip install -r requirements.txt'.format(DEPLOY_DIR))


def _migrate():
    _run_env('cd {}; python manage.py migrate --noinput'.format(DEPLOY_DIR))


def _collect_static():
    _run_env('cd {}; python manage.py collectstatic --noinput'.format(DEPLOY_DIR))


def _make_link():
    _run_web('rm {} || echo "ignore"'.format(CURRENT_DIR))
    _run_web('ln -sn {} {}'.format(DEPLOY_DIR, CURRENT_DIR))


def _restart_supervisor():
    _run_web("chmod +x {}/server/gunicorn.sh".format(CURRENT_DIR))
    run("supervisorctl -c %s/server/supervisor.conf reload || echo 'fail to reload supervisor'" % CURRENT_DIR)
    run("supervisorctl -c %s/server/supervisor.conf restart all || supervisord -c %s/server/supervisor.conf" % (
        CURRENT_DIR, CURRENT_DIR))


def _restart_nginx():
    run('cp {}/server/nginx.conf /etc/nginx/sites-enabled/www.conf'.format(DEPLOY_DIR))
    run('service nginx restart')

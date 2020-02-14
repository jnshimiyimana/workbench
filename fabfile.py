import tempfile

from fabric.api import cd, env, execute, local, run, task
from fabric.contrib.project import rsync_project


env.forward_agent = True
env.hosts = ["deploy@workbench.feinheit.ch"]
WORKBENCH = ["fh", "dbpag", "bf", "test"]


@task
def check():
    local("venv/bin/flake8 .")
    local("yarn run check")


@task
def dev():
    with tempfile.NamedTemporaryFile() as f:
        # https://gist.github.com/jiaaro/b2e1b7c705022c2cf56888152a999f65
        f.write(
            """\
trap "exit" INT TERM
trap "kill 0" EXIT

PYTHONWARNINGS=always venv/bin/python manage.py runserver 0.0.0.0:%(port)s &
HOST=%(host)s yarn run dev &

for job in $(jobs -p); do wait $job; done
"""
            % {"port": 8000, "host": "127.0.0.1"}
        )
        f.flush()

        local("bash %s" % f.name)


def _do_deploy(folder, rsync):
    with cd(folder):
        run("git checkout master")
        run("git fetch origin")
        run("git merge --ff-only origin/master")
        run('find . -name "*.pyc" -delete')
        run("venv/bin/pip install -U pip wheel setuptools")
        run("venv/bin/pip install -r requirements.txt")
        for wb in WORKBENCH:
            run("DOTENV=.env/{} venv/bin/python manage.py migrate".format(wb))
        if rsync:
            rsync_project(
                local_dir="static/", remote_dir="%sstatic/" % folder, delete=True
            )
        run(
            "DOTENV=.env/{} venv/bin/python manage.py collectstatic --noinput".format(
                WORKBENCH[0]
            )
        )


def _restart_all():
    for wb in WORKBENCH:
        run("systemctl --user restart workbench@{}".format(wb))


@task
def deploy():
    check()
    local("git push origin master")
    local("yarn run prod")
    _do_deploy("www/workbench/", rsync=True)
    _restart_all()


@task
def deploy_code():
    check()
    local("git push origin master")
    _do_deploy("www/workbench/", rsync=False)
    _restart_all()


@task
def pull_database(namespace):
    remote = {"fh": "workbench", "dbpag": "dbpag-workbench", "bf": "bf-workbench"}[
        namespace
    ]
    local("dropdb --if-exists workbench")
    local("createdb workbench")
    local(
        'ssh root@workbench.feinheit.ch "sudo -u postgres pg_dump -Fc %s"'
        " | pg_restore -Ox -d workbench" % remote
    )


@task(alias="mm")
def makemessages():
    local(
        "venv/bin/python manage.py makemessages -a -i venv -i htmlcov"
        " --add-location file"
    )
    local(
        "venv/bin/python manage.py makemessages -a -i venv -i htmlcov"
        " --add-location file"
        " -i node_modules -i lib"
        " -d djangojs"
    )


@task(alias="cm")
def compilemessages():
    local("cd conf && ../venv/bin/python ../manage.py compilemessages")


@task
def update_requirements():
    local("rm -rf venv")
    local("python3 -m venv venv")
    local("venv/bin/pip install -U pip wheel setuptools")
    local("venv/bin/pip install -U -r requirements-to-freeze.txt --pre")
    execute("freeze")


@task
def freeze():
    local(
        '(printf "# AUTOGENERATED, DO NOT EDIT\n\n";'
        "venv/bin/pip freeze -l"
        # Until Ubuntu gets its act together:
        ' | grep -vE "(^pkg-resources)"'
        ") > requirements.txt"
    )


@task
def setup():
    local("python3 -m venv venv")
    execute("update")


@task
def update():
    local("venv/bin/pip install -U pip wheel")
    local("venv/bin/pip install -r requirements.txt")
    local("yarn")
    local("venv/bin/python manage.py migrate")

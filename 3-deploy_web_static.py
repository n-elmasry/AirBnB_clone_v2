#!/usr/bin/python3
"""creates and distributes an archive to your web servers"""
from fabric.api import put, run, local, env
from datetime import datetime
from os import path


env.hosts = ['100.26.153.239', '3.90.82.110']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """generates a .tgz archive """
    local("mkdir -p versions")
    time_now = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = "versions/web_static_{}.tgz".format(time_now)
    result = local("tar -czf {} web_static/".format(file_path))
    if result.failed:
        return None
    return (file_path)


def do_deploy(archive_path):
    """Distribute an archive to your web servers"""
    try:

        if path.exists(archive_path) is False:
            return False
        put(archive_path, '/tmp/')

        archive_name = archive_path.split('/')[-1]
        foldername = archive_name.split('.')[0]

        run("sudo mkdir -p /data/web_static/releases/{}/".format(foldername))

        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            archive_name, foldername))

        run("sudo rm /tmp/{}".format(archive_name))

        run("sudo mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/".format(foldername, foldername))

        run("sudo rm -rf /data/web_static/releases/{}/web_static"
            .format(foldername))

        run("sudo rm -rf /data/web_static/current")

        run("sudo ln -s /data/web_static/releases/{}/ \
            /data/web_static/current".format(foldername))

        return True
    except Exception as e:
        return False


def deploy():
    """creates and distributes an archive to your web servers"""
    archive_path = do_pack()

    if archive_path is None:
        return False
    return do_deploy(archive_path)

#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""

from fabric.api import put, run, env
from os import path


env.hosts = ['52.3.220.66', '100.26.232.118']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


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
        print("New version deployed!")

        return True
    except Exception as e:
        return False

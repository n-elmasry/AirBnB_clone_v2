#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""
from fabric.contrib import files
from fabric.api import env, put, run
import os

env.hosts = ['100.26.153.239', '3.90.82.110']


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False

    data_path = '/data/web_static/releases/'
    tmp = archive_path.split('.')[0]
    name = tmp.split('/')[1]
    destination = data_path + name

    try:
        put(archive_path, '/tmp')
        run('sudo mkdir -p {}'.format(destination))
        run(f'sudo tar -xzf /tmp/{name}.tgz -C {destination}')
        run(f'sudo rm -f /tmp/{name}.tgz')
        run(f'sudo mv {destination}/web_static/* {destination}/')
        run(f'sudo rm -rf {destination}/web_static')
        run(f'sudo rm -rf /data/web_static/current')
        run(f'sudo ln -s {destination} /data/web_static/current')
        return True
    except Exception as e:
        return False

#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the web_static folder """
from fabric.api import local
from datetime import datetime


def do_pack():
    """generates a .tgz archive """
    local("mkdir -p versions")
    time_now = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = "versions/web_static_{}.tgz".format(time_now)
    result = local("tar -czf {} web_static/".format(file_path))
    if result.failed:
        return None
    return (file_path)

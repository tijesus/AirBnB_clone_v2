#!/usr/bin/python3
"""
Deletes out-of-date archives
fab -f 100-clean_web_static.py do_clean:number=2
    -i ssh-key -u ubuntu > /dev/null 2>&1
"""

import os
from fabric.api import *

env.hosts = ['54.157.158.3', '54.146.71.138']


def do_clean(number=0):
    """Delete out-of-date archives.
        If number is 0 or 1, keeps only the most recent archive. If
        number is 2, keeps the most and second-most recent archives,
        etc.
    """
    n = int(number)
    keep_one = 'ls -t | tail -n +2 | xargs rm -rfv'
    keep_n = 'ls -t | tail -n +{} | xargs rm -rfv'

    with lcd('versions'):
        if n == 0 or n == 1:
            local(keep_one)
        else:
            local(keep_n.format(n + 1))

    with cd('/data/web_static/releases/'):
        if n == 0 or n == 1:
            run(keep_one)
        else:
            run(keep_n.format(n + 1))

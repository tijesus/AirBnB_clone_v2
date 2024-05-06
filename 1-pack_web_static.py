#!/usr/bin/python3
from fabric import task
import sys

@task
def my_task(c):
    c.run("ls -l")

if __name__ == "__main__":
    my_task(sys.argv[1])
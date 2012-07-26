import os


def local(cmd):
    print cmd
    os.system(cmd)

local("python setup.py sdist")
#local("python setup.py sdist upload")

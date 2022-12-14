# This file is placed in the Public Domain.


"setuptools"


import os


from setuptools import setup


def read():
    return open("README.rst", "r").read()


def uploadlist(dir):
    upl = []
    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if os.path.isdir(d):   
            upl.extend(uploadlist(d))
        else:
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)
    return upl


setup(
    name="jsonbot",
    version="100",
    author="Bart Thate",
    author_email="bthate@dds.nl",
    url="http://github.com/bhate/jsonbot",
    description="The JSON Every Where Bot",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    packages=["jsonbot", "jsonbot.mod"],
    include_package_data=True,
    data_files=[
                ("jsonbot", ["files/jsonbot.service",])
                ("share/doc/jsonbot", ["README.rst"])
               ],
    scripts=[
             "bin/jsonbot",
             "bin/jsonbotcmd",
             "bin/jsonbotctl",
             "bin/jsonbotd"
            ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: Public Domain",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: System Administrators",
        "Topic :: Communications :: Chat :: Internet Relay Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
     ],
)

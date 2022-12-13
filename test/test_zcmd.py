# This file is placed in the Public Domain.
# pylint: disable=E1101,C0116,W0613


"tinder"


import os
import random
import shutil
import sys
import termios
import time
import traceback
import unittest
import _thread


sys.path.insert(0, os.getcwd())


from jsonbot import Cfg, Command, Event, Handler, Object, Wd
from jsonbot import launch, parse, scan, update
from jsobbot import elapsed, name
from jsonbot import locked
from jsonbot import cmds, info, irc, log, rss, todo


Wd.workdir = ".test"
Cfg.debug = True


scan(cmds)
scan(info)
scan(irc)
scan(log)
scan(rss)
scan(todo)


errors = []
events = []
results = []


param = Object()
param.add = ["test@shell", "bart", ""]
param.cfg = ["server=localhost", ""]
param.dne = ["test4", ""]
param.rem = ["reddit", ""]
param.dpl = ["reddit title,summary,link", ""]
param.flt = ["0", ""]
param.fnd = [
             "cfg",
             "log",
             "rss",
             "log txt==test",
             "cfg server==localhost",
             "rss rss==reddit"
            ]
param.log = ["test1", ""]
param.nme = ["reddit reddit"]
param.dpl = ["reddit title,link"]
param.rem = ["reddit"]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.tdo = ["test4", ""]
param.thr = [""]



class CLI(Handler):

    def raw(self, txt):
        if Cfg.verbose:
            cprint(txt)


def boot(txt):
    parse(txt)
    if "c" in Cfg.opts:
        Cfg.console = True
    if "d" in Cfg.opts:
        Cfg.daemon = True
    if "v" in Cfg.opts:
        Cfg.verbose = True
    if "w" in Cfg.opts:
        Cfg.wait = True
    if "x" in Cfg.opts:
        Cfg.exec = True


def consume(evts):
    fixed = []
    res = []
    for evt in evts:
        evt.wait()
        fixed.append(evt)
    for fff in fixed:
        try:
            evts.remove(fff)
        except ValueError:
            continue
    return res


def cprint(txt):
    print(txt)
    sys.stdout.flush()



class TestCommands(unittest.TestCase):

    def setUp(self):
        boot(" ".join(sys.argv[1:]))
        cprint(Cfg)
        
    def test_commands(self):
        cli = CLI()
        cmds = sorted(Command.cmd)
        for cmd in cmds:
            for ex in getattr(param, cmd, ""):
                evt = Event()
                evt.channel = "#jsonbot"
                evt.orig = repr(cli)
                txt = cmd + " " + ex
                evt.txt = txt.strip()
                cli.handle(evt)
                events.append(evt)
        consume(events)
        self.assertTrue(not events)

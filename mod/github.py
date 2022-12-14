import logging
import re

from jsonbot.lib.callbacks import callbacks
from jsonbot.lib.commands import cmnds
from jsonbot.lib.examples import examples
from jsonbot.lib.persist import PlugPersist
from jsonbot.plugs.common.tinyurl import get_tinyurl
from jsonbot.utils.exception import handle_exception

gitHashRule = re.compile(r".*\b([0-9a-f]{7,40})\b.*")

try:
    from github2.client import Github

    gh = Github()
    gotit = True
except ImportError:
    gotit = False
    logging.warn("github2 is not installed. see https://github.com/ask/python-github2")

cfg = PlugPersist("github", {})


def f_find_github_commit(phenny, input):
    print("Searching for commit...", input)
    query = input.group(1)
    _find_github_commit(phenny, query)


def _find_github_commit(phenny, query):
    pass


def containsHash(bot, ievent):
    if ievent.how == "backgound":
        return 0
    if ievent.channel in cfg.data and len(cfg.data[ievent.channel]):
        if gitHashRule.match(ievent.txt):
            return 1
    return 0


def doLookup(bot, ievent):
    fnd = gitHashRule.match(ievent.txt)
    for project in cfg.data[ievent.channel]:
        try:
            res = gh.commits.show(project, sha=fnd.group(1))
            logging.info("response from github: %s" % res)
            bot.say(
                ievent.channel,
                "%s- %s by %s: %s %s"
                % (
                    project,
                    res.id[:7],
                    res.author["name"],
                    res.message[:60],
                    get_tinyurl("https://github.com" + res.url)[0],
                ),
            )
            return
        except:
            print("Couldn't find %s" % fnd.group(1))


if gotit:
    callbacks.add("PRIVMSG", doLookup, containsHash, threaded=True)
    callbacks.add("CONSOLE", doLookup, containsHash, threaded=True)
    callbacks.add("MESSAGE", doLookup, containsHash, threaded=True)
    callbacks.add("DISPATCH", doLookup, containsHash, threaded=True)
    callbacks.add("TORNADO", doLookup, containsHash, threaded=True)


def handle_gh_commit_lookup_enable(bot, ievent):
    """no arguments - enable github commit lookups in a channel."""
    if len(ievent.args) != 1:
        ievent.reply(
            "syntax: gh_commit_lookup_enable user/project (e.g. firebreath/FireBreath)"
        )
        return
    if ievent.channel not in cfg.data:
        cfg.data[ievent.channel] = []
    project = ievent.args[0]
    cfg.data[ievent.channel].append(project)
    cfg.save()
    ievent.reply("github lookups enabled for %s" % project)


if gotit:
    cmnds.add("gh_commit_lookup_enable", handle_gh_commit_lookup_enable, ["OPER"])
    examples.add(
        "gh_commit_lookup_enable",
        "enable github commit lookups in the channel",
        "gh_commit_lookup_enable",
    )


def handle_gh_commit_lookup_disable(bot, ievent):
    """no arguments - disable github commit lookups in a channel."""
    cfg.data[ievent.channel] = []
    cfg.save()
    ievent.reply("github lookups disabled")


if gotit:
    cmnds.add("gh_commit_lookup_disable", handle_gh_commit_lookup_disable, ["OPER"])
    examples.add(
        "gh_commit_lookup_disable",
        "disable github commit lookups in the channel",
        "gh_commit_lookup_disable",
    )

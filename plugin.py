###
# Copyright (c) 2020, mogad0n
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

from supybot import utils, plugins, ircutils, callbacks, ircmsgs, conf, world, log
from supybot.commands import *
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Etoke')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

import random
import pickle
import sys
import time

colorp = "\00309,01"

currentEtokes = []


filename = conf.supybot.directories.data.dirize("Etoke.db")

class Etoke(callbacks.Plugin):
    """Pass the doob idiot"""
    threaded = True


    def __init__(self, irc):
        self.__parent = super(Etoke, self)
        self.__parent.__init__(irc)
        self.db = {}
        self._loadDb()
        world.flushers.append(self._flushDb)

    def _loadDb(self):
        """Loads the (flatfile) database mapping nicks to optins."""

        try:
            with open(filename, "rb") as f:
                self.db = pickle.load(f)
        except Exception as e:
            self.log.debug("Etoke: Unable to load pickled database: %s", e)

    def _flushDb(self):
        """Flushes the (flatfile) database mapping nicks to optins."""

        try:
            with open(filename, "wb") as f:
                pickle.dump(self.db, f, 2)
        except Exception as e:
            self.log.warning("Etoke: Unable to write pickled database: %s", e)

    def die(self):
        self._flushDb()
        world.flushers.remove(self._flushDb)
        self.__parent.die()

    def optin(self, irc, msg, args):
        """This command takes no arguments

        Added the caller to etokers group
        """
        nick = msg.nick
        self.db[nick] = ""
        irc.reply(colorp + f'{nick} will be notified during etokes')

    optin = wrap(optin)

    def optout(self, irc, msg, args):
        """This command takes no arguments

        Removes caller from the etokers group
        and will also reset their stats
        """
        nick = msg.nick
        del self.db[nick]
        irc.reply(colorp + f'{nick} will no longer be notified of etoke events and their stats are reset')

    optout = wrap(optout)

    @wrap(['channel'])
    def etoke(self, irc, msg, args, channel):
        """
        Starts an etoke and adds you do the tokers group. Use to @join the etoke,
        @tokers to see who is in the etoke, Use @notify to intimate others about an toke in progress! @optin to sign up for pings.
        By default everyone is opted out. Use @ready to start right away
        """
        if len(currentEtokes) == 0:
            irc.reply('No Etokes on this channel atm bro. I\'ll make one for you')
        nick = msg.nick
        self.db[nick] = ""
        if nick in currentEtokes:
            irc.reply("HEY ASSHOLE YOU'RE ALREADY IN THE ETOKE")
            return
        for nicks in self.db:
            currentEtokes.append(nicks)
        tokers = " ".join(currentEtokes)
        irc.reply(colorp + f'{nick} has called for an ETOKE! {tokers} assemble! type @join to join them. Auto-Etoke will commence in 2-mins')
        time.sleep(120)
        tokers = " ".join(currentEtokes)
        irc.reply(f'Get read to BLAZE! {tokers}!')
        irc.reply(colorp + "5.....")
        time.sleep(1)
        irc.reply(colorp + "4.....")
        time.sleep(1)
        irc.reply(colorp + "3.....")
        time.sleep(1)
        irc.reply(colorp + "2.....")
        time.sleep(1)
        irc.reply(colorp + "1.....")
        time.sleep(1)
        a = str(random.randrange(0,16))
        b = str(random.randrange(0,16))
        while a == b:
            a = str(random.randrange(0,16))
        irc.reply("\002\003" + a + "," + b + "ETOKE" + "\003" + b + "," + a + "ETOKE" + "\003" + a + "," + b + "ETOKE")
        irc.reply("\002\003" + b + "," + a + "ETOKE" + "\003" + a + "," + b + "ETOKE" + "\003" + b + "," + a + "ETOKE")
        irc.reply("\002\003" + a + "," + b + "ETOKE" + "\003" + b + "," + a + "ETOKE" + "\003" + a + "," + b + "ETOKE")


    def join(self, irc, msg, args):
        """This command takes no arguments

        Join the circle and get ready to get blazed.
        This automatically opts you in for further notifs.
        """
        nick = msg.nick
        self.db[nick]
        currentEtokes.append(nick)
        irc.reply(colorp + f'{nick} has joined the session type @join to partake')
    join = wrap(join)



Class = Etoke


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

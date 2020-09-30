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

import thread
import random
import pickle
import sys
import time

colorp = "\00309,01"

tokes = 0


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
        channel = msg.channel
        nick = msg.nick
        self.db[channel] = nick
        irc.reply(colorp + f'{nick} will be notified during etokes')

    optin = wrap(optin)

    def optout(self, irc, msg, args):
        """This command takes no arguments

        Removes caller from the etokers group
        and will also reset their stats
        """
        channel = msg.channel
        nick = msg.nick
        del self.db[channel]
        irc.reply(colorp + f'{nick} will no longer be notified of etoke events on {channel} and their stats are reset')

    optout = wrap(optout)


    def etoke(self, irc, msg, args):
        """This command takes no arguments

        Starts an etoke and adds you do the tokers group. Use @imin to join the etoke,
        @optin to sign up for pings. By default everyone is opted out.
        Use @start to start right away
        """
        nick = msg.nick
        channel = msg.channel
        if channel in self.db:
            irc.reply(colorp + f'THERES ALREADY AN ETOKE on {channel} YOU IDIOT!!!!')
        else:
            self.db[channel] = list([nick])
            tokers = " ".join(nick)
        thread.start_new_thread(etokeExpire, (chan, irc.reply))
        irc.reply(colorp + f'{nick} has called for an ETOKE! _\\|/_ ( .__.) . o O {tokers} assemble! type @imin to join in. Auto-Etoke will commence in 2-mins. @start to commence')
    etoke = wrap(etoke)


    def imin(self, irc, msg, args):
        """This command takes no arguments

        Join the circle and get ready to get blazed.
        This automatically opts you in for further notifs.
        """
        channel = msg.channel
        nick = msg.nick
        if channel in self.db:
            if nick in self.db[channel]:
                irc.reply(colorp + "HEY ASSHOLE YOU'RE ALREADY IN THE ETOKE")
            else:
                self.db[channel].append(nick)
                irc.reply(colorp + nick + " has joined the etoke! Type !imin to join them!")
        else:
            irc.reply(colorp + "NO ETOKE ON THIS CHANNEL ATM BRO ILL MAKE ONE FOR YOU H/O")
            return etoke(self, irc, msg, args)
    imin = wrap(imin)

    def blaze(self, irc, msg, args):
        """
        Just spark it bro
        """
        nick = msg.nick
        channel = msg.channel
        if channel in self.db:
            if self.db[channel][0] == nick:
                irc.reply(colorp + " ".join(self.db[channel]) + " get your lighters ready!! It's time to smoke weed in....")
                del self.db[channel]
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
            else:
                irc.reply(colorp + "Stop trying to steal " + self.db[channel][0] + "'s etoke!! Use @blaze confirm if you think they've fallen asleep!")
        else:
            irc.reply(colorp + "NO ETOKE ON THIS CHANNEL ATM BRO")
    blaze = wrap(blaze)

    def etokeExpire(self, irc, msg, args):
        channel = msg.channel
        for x in range(0,15):
            if x == 10:
                irc.reply(colorp + "Oh no " + " ".join(self.db[channel]) + "!! There's only 1 minute left in the etoke! Bug " + self.db[channel][0] + " to start it or use @blaze to confirm!")
            time.sleep(60)
            if channel not in self.db:
                return
        del self.db[channel]
        irc.reply(colorp + "etoke expired!! MOTHERFUCKING BASTARDS!!")


    def top5(inp, input=None, db=None, irc.reply=None):
        db_init(db)
        top = db.execute("select nick,count from etokestats"
                    " where chan = ? ORDER by count DESC limit 5",
                    (input.chan,))
        if top:
            top_list = top.fetchall()
        else:
            return colorp + "Nobody has toked yet :("

        if not top_list:
            return colorp + "Nobody has toked yet :(("

        irc.reply(colorp + "Top 5 tokers:")

        i = 1

        for entry in top_list:
            irc.reply(colorp + "%i. %s - %i" % (i, entry[0], entry[1]))
            i = i + 1





Class = Etoke


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

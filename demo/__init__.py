# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from os.path import dirname, join
from os import listdir
import re

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.util import play_mp3

__author__ = 'eward'

LOGGER = getLogger(__name__)


class DemoSkill(MycroftSkill):

    def __init__(self):
        super(DemoSkill, self).__init__(name="DemoSkill")
        self.process = None

    def initialize(self):
        self.load_data_files(dirname(__file__))

        for name in listdir(join(dirname(__file__), "mp3")):
            name = re.sub(".mp3", "", name)
            name = re.sub("_", " ", name)
            self.register_vocabulary(name, "SongTitle")

        #mouthful_intent = IntentBuilder("MouthfulIntent").\
        #    require("MouthfulKeyword").build()
        #self.register_intent(mouthful_intent, self.handle_mouthful_intent)

        #collapse_intent = IntentBuilder("CollapseIntent").\
        #    require("CollapseKeyword").build()
        #self.register_intent(collapse_intent,
        #                     self.handle_collapse_intent)

        play_song_intent = IntentBuilder("PlaySongIntent").\
            require("PlayKeyword").require("SongTitle").build()
        self.register_intent(play_song_intent,
                             self.handle_play_song_intent)

    def handle_mouthful_intent(self, message):
        self.speak_dialog("mouthful")
        self.process = play_mp3(join(dirname(__file__),"MouthfulOfDiamonds.mp3")) 

    def handle_collapse_intent(self, message):
        self.speak_dialog("collapse")
        self.process = play_mp3(join(dirname(__file__),"SpeedTheCollapse.mp3"))

    def handle_play_song_intent(self, message):
        title = message.metadata.get("SongTitle")
        self.speak_dialog("play.song", {'title': title})
        title += ".mp3"
        title = re.sub(" ", "_", title)
        self.process = play_mp3(join(dirname(__file__),"mp3",title))

    def stop(self):
        if self.process:# and self.process.poll() is None:
            self.speak_dialog('music.stop')
            self.process.terminate()
            self.process.wait()


def create_skill():
    return DemoSkill()

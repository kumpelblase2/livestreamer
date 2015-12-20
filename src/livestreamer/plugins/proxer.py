import re
import json

from livestreamer.plugin import Plugin
from livestreamer.plugin.api import http, validate
from livestreamer.stream import HTTPStream

_url_re = re.compile("http(s)?://proxer.me/watch/(?P<anime>\d+)/(\d+)/(engsub|gersub)(#.+)?")

_players_re = re.compile("streams = (\[.*\]);")
_video_src_re = re.compile('<source type="video\/mp4" src="(.+)">')

class Proxer(Plugin):
    @classmethod
    def can_handle_url(self, url):
        return _url_re.match(url)

    def _get_streams(self):
        stream_name = _url_re.match(self.url).group('anime')
        res = http.get(self.url)
        players_match = _players_re.search(res.text).group(1)
        streams = json.loads(players_match)
        
        for stream in filter((lambda x: x["name"] == "Proxer-Stream"), streams):
            video_page_url = stream["replace"].replace('#', stream["code"])
            video_page = http.get(video_page_url)
            video_url = _video_src_re.search(video_page.text).group(1)
            yield stream_name, HTTPStream(self.session, video_url)

__plugin__ = Proxer

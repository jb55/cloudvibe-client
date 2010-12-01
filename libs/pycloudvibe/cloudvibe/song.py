
from mutagen.mp3 import EasyMP3
import os

class Song():
  
  def __init__(self, path):
    self.path = path
    self.filename = os.path.split(path)[1]

  def load_tags(self):
    audio = EasyMP3(self.path)

    self.album = ''
    self.artist = ''
    self.title = ''

    if audio.has_key("artist"):
      self.artist = audio["artist"][0]

    if audio.has_key("title"):
      self.title = audio["title"][0]

    if audio.has_key("album"):
      self.album = audio["album"][0]


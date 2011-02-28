
from mutagen.mp3 import EasyMP3
import hashlib
import json
import os

class Song():
  
  def __init__(self, path):
    self.path = path
    self.filename = os.path.split(path)[1]
    self.info = {}

  def toDict(self):
    return { "filename": self.filename
           , "artist": self.info["artist"]
           , "title": self.info["title"]
           , "album": self.info["album"]
           , "md5": self.md5
           }

  def load_all(self):
    self.load_tags()
    self.load_md5()

  def load_md5(self):
    data = open(self.path).read()
    md5 = hashlib.md5()
    md5.update(data)
    self.md5 = md5.hexdigest()

  def load_tags(self):
    audio = EasyMP3(self.path)

    self.info["album"] = ''
    self.info["artist"] = ''
    self.info["title"] = ''

    if audio.has_key("artist"):
      self.info["artist"] = audio["artist"][0]

    if audio.has_key("title"):
      self.info["title"] = audio["title"][0]

    if audio.has_key("album"):
      self.info["album"] = audio["album"][0]


class SongJsonEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Song):
      return obj.toDict()
    else:
      return json.JSONEncoder.default(self, obj)

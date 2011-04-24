
from sqlalchemy import *
from mutagen.mp3 import EasyMP3
from cloudvibe import util
import hashlib
import json
import os

def sync_key(songs):
  return map(lambda s: s.md5, songs)


class Song(object):

  def __repr__(self):
    tagrep = " ".join([self.artist, "-", self.title])
    rep = tagrep if self.hasTitle() else self.filename
    return "<Song: " + rep + ">"


  def __init__(self, path):
    self.path = path
    self.filename = os.path.split(path)[1]
    self.md5_changed = False

  def toDict(self):
    return { "filename": self.filename
           , "artist": self.artist
           , "title": self.title
           , "album": self.album
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

    self.album = ''
    self.artist = ''
    self.title = ''

    if audio.has_key("artist"):
      self.artist = audio["artist"][0]

    if audio.has_key("title"):
      self.title = audio["title"][0]

    if audio.has_key("album"):
      self.album = audio["album"][0]

  def write_tags(self):
    audio = EasyMP3(self.path)

    if audio.has_key("artist"):
      audio["artist"] = self.artist

    if audio.has_key("title"):
      audio["title"] = self.title

    if audio.has_key("album"):
      audio["album"] = self.album
    
    audio.save()
    
    self.load_md5()
    self.md5_changed = True


  def hasTitle(self):
    return bool(self.artist and self.title)




class SongJsonEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Song):
      return obj.toDict()
    else:
      return json.JSONEncoder.default(self, obj)


def get_all_local_songs(db):
  """ Gets all of the songs that are stored in the database """
  return db.session.query(Song).all()


def insert_songs(db, songs):
  """ Inserts songs into the database """
  table = db.song
  db.session.add_all(songs)
  db.session.commit()


def sync_local_db(db, songs):
  """ Syncs a list of songs with the local database """
  table = db.song
  sel = table.select()
  rs = sel.execute()

  db_md5s = sync_key(rs)
  md5s = sync_key(songs)
  shared_md5s = util.intersect(db_md5s, md5s)
  db_missing = util.difference(shared_md5s, md5s)
  local_missing = util.difference(shared_md5s, db_md5s)

  songs_to_add = filter(lambda s: s.md5 in db_missing, songs)
  insert_songs(db, songs_to_add)

  print "Missing songs", songs_to_add
  print "Shared md5s", shared_md5s




from sqlalchemy import *
from mutagen.mp3 import EasyMP3
from mutagen.id3 import ID3
from cloudvibe import util
from cloudvibe.settings import DEFAULT_SONG_DIR
import sys
import hashlib
import json
import os

SONG_COLS = [
  Column('id', Integer, primary_key=True)
, Column('album', String(128))
, Column('artist', String(128))
#, Column('bpm', Integer)
, Column('comments', String(2048))
, Column('composer', String(128))
, Column('filename', String(128))
, Column('genre', String(32))
, Column('img', String(36))
, Column('label', String(128))
, Column('md5', String(32))
, Column('old_md5', String(32))
, Column('modified', Integer)
, Column('path', String(128))
, Column('publisher', String(128))
#, Column('release_date', DateTime)
, Column('studio', String(128))
, Column('title', String(512))
#, Column('track', Integer)
, Column('uid', String(36))
, Column('user_id', Integer)
#, Column('year', Integer)
]

VALID_KEYS = (
  "album",
  "bpm",
  "compilation", # iTunes extension
  "composer",
  "copyright",
  "encodedby",
  "lyricist",
  "length",
  "media",
  "mood",
  "title",
  "version",
  "artist",
  "performer",
  "conductor",
  "arranger",
  "discnumber",
  "organization",
  "tracknumber",
  "author",
  "albumartistsort", # iTunes extension
  "albumsort",
  "composersort", # iTunes extension
  "artistsort",
  "titlesort",
  "isrc",
  "discsubtitle",
)

def sync_key(songs):
  return map(lambda s: s.md5, songs)


class Song(object):

  def __repr__(self):
    tagrep = " ".join([self.artist or "?", "-", self.title or "?"])
    rep = tagrep if self.hasTitle() else self.filename
    return "<Song: " + rep + ">"


  def __init__(self, path):
    self.path = path
    self.filename = os.path.split(path)[1]
    self.md5_changed = False


  def fields(self):
    cols = map(lambda c: c.name, SONG_COLS)
    return filter(lambda n: n not in ("id", "path"), cols)


  def toDict(self):
    d = {}
    fields = self.fields()
    for field in fields:
      val = getattr(self, field)
      if val:
        d[field] = val
    return d


  def fromDict(self, d):
    fields = util.intersect(self.fields(), d.keys())
    for field in fields:
      setattr(self, field, d[field])


  def load_all(self):
    self.load_tags()
    self.load_md5()


  def load_md5(self):
    data = None
    try:
      data = open(self.path).read()
    except:
      return 

    md5 = hashlib.md5()
    md5.update(data)
    self.md5 = md5.hexdigest()


  def load_dict_tags(self, data):
    self.fromDict(data)


  def load_tags(self):
    audio = None
    try:
      audio = EasyMP3(self.path)
    except:
      return

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
    try:
      tags = ID3(self.path)
    except:
      tags = ID3()

    fields = filter(lambda f: f in VALID_KEYS, self.fields())

    for field in fields:
      data = getattr(self, field)
      setattr(tags, field, data)

    tags.save(self.path)

    self.old_md5 = self.md5
    self.load_md5()
    self.modified = 1


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

  db_songs = [song for song in rs]
  db_md5s = sync_key(db_songs)
  md5s = sync_key(songs)
  shared_md5s = util.intersect(db_md5s, md5s)
  db_missing = util.difference(shared_md5s, md5s)
  local_missing = util.difference(shared_md5s, db_md5s)

  deleted = filter(lambda s: s.uid in local_missing, db_songs)
  songs_to_add = filter(lambda s: s.md5 in db_missing, songs)
  insert_songs(db, songs_to_add)

  print "Missing songs", songs_to_add
  print "Shared md5s", shared_md5s

  return deleted

def find_songs(dirs):
  """ Returns a list of songs in the given directories """
  files = []
  for dir in dirs:
    for dirpath, dirnames, filenames in os.walk(dir):
      for filename in [f for f in filenames if f.endswith(".mp3")]:
        files.append(os.path.join(dirpath, filename).encode("utf-8"))
  return files


def song_dirs():
  default = [DEFAULT_SONG_DIR]
  map(util.ensure_path, default)
  return default
  f = lambda: default

  if sys.platform == 'darwin':
    from cloudvibe.platform.darwin.paths import song_dirs
    f = song_dirs
  elif sys.platform == 'win32':
    from cloudvibe.platform.win32.paths import song_dirs
    f = song_dirs

  dirs = f()

  if len(dirs) == 0:
    dirs = default

  map(util.ensure_path, dirs)

  return dirs


def default_song_dir():
  default = DEFAULT_SONG_DIR
  util.ensure_path(default)
  return default
  f = lambda: default

  if sys.platform == 'darwin':
    from cloudvibe.platform.darwin.paths import default_song_dir
    f = default_song_dir
  elif sys.platform == 'win32':
    from cloudvibe.platform.win32.paths import default_song_dir
    f = default_song_dir

  d = f() or default

  util.ensure_path(d)

  return d

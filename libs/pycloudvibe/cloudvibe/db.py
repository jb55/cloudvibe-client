
from sqlalchemy import *
from sqlalchemy.orm import mapper, sessionmaker, relationship
import config
import os
import util
from song import *
from playlist import *


class Database():
  def __init__(self, engine, conf=config.DEFAULT):
    self.db = engine
    self.meta = MetaData(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    self.session = Session()

    playlist_table = Table('playlist', self.meta, *PLAYLIST_COLS)
    self.playlist = playlist_table

    playlist_to_song = Table('playlist_to_song', self.meta, *PLAYLIST_SONG_COLS)

    song_table = Table('song', self.meta, *SONG_COLS)
    self.song = song_table

    mapper(Playlist, playlist_table, properties={
        'children': relationship(Song, secondary=playlist_to_song)
    })
    mapper(Song, song_table)

    init_db(self.meta)


def init_db(metadata, conf=config.DEFAULT):
  db_file = conf.get('db_file')
  if not os.path.exists(db_file):
    metadata.create_all()


def get_db(conf=config.DEFAULT):
  util.init_fs(conf)
  cs = conf.get('db_engine')
  engine = create_engine(cs)
  db = Database(engine, conf)
  return db



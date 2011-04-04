
from sqlalchemy import *
from sqlalchemy.orm import mapper, sessionmaker
import config
import os
import util
from song import Song


SONG_COLS = [
  Column('id', Integer, primary_key=True)
, Column('user_id', Integer)
, Column('modified', String(512))
, Column('year', DateTime)
, Column('bpm', Integer)
, Column('track', Integer)
, Column('title', String(512))
, Column('comments', String(2048))
, Column('genre', String(32))
, Column('composer', String(128))
, Column('album', String(128))
, Column('artist', String(128))
, Column('md5', String(32))
, Column('filename', String(128))
]


class Database():
  def __init__(self, engine, conf=config.DEFAULT):
    self.db = engine
    self.meta = MetaData(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    self.session = Session()

    # Setup table mappings
    #  Song
    song_table = Table('song', self.meta, *SONG_COLS)
    mapper(Song, song_table)
    self.song = song_table

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



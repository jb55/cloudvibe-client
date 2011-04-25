from sqlalchemy import *
from cloudvibe import util
import sys
import os

PLAYLIST_COLS = [
  Column('id', Integer, primary_key=True)
, Column('name', String(512))
, Column('modified', Integer)
]

PLAYLIST_SONG_COLS = [
  Column('playlist_id', Integer, ForeignKey('playlist.id'))
, Column('song_id', Integer, ForeignKey('song.id'))
]

class Playlist(object):
  
  def __init__():
    pass

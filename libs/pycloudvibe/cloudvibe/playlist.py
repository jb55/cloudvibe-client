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
  
  def __init__(self, name):
    self.name = name


  def addSongs(self, songs):
    for i in range(len(songs)):
      self.children.append(songs[i]) 

  def removeSongs(self, songs):
    for i in range(len(self.children)):
      if self.children[i] in songs:
        del self.children[i]
        
  def getAllSongs(self):
    return self.children

  def getAllSongNames(self):
    songs = []
    for i in range(len(self.children)):
      songs.append(self.children[i].title) 
    
    return songs

  def removeAllSongs(self):
    for i in range(len(self.children)):
      del self.children[i]


def createPlaylist(db, pl_name, songs=[]):
  pl = Playlist(pl_name)
  pl.addSongs(songs)
  db.session.add(pl)
  db.session.commit()


def deletePlaylist(db, pl_name):
  pl = db.session.query(Playlist).filter_by(name=pl_name).all()[0]
  pl.removeAllSongs()
  db.session.delete(pl)
  db.session.commit()


def getAllLocalDBPlaylists(db):
  pl_tmp = db.session.query(Playlist).all()
  playlists = []
  for i in range(len(pl_tmp)):
    playlists.append(pl_tmp[i].name)

  return playlists


def getLocalDBPlaylist(db, pl_name):
  return db.session.query(Playlist).filter_by(name=pl_name).all()[0]

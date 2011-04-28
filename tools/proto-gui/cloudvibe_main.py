import webbrowser 
import cloudvibe.db
from cloudvibe.api import API
from cloudvibe.song import Song, get_all_local_songs, sync_local_db, insert_songs
from cloudvibe.song import song_dirs, find_songs
from cloudvibe.gui import Tray
from cloudvibe.playlist import *

DB = cloudvibe.db.get_db()

def get_db():
  return DB


def get_paths():
  return MONITOR_PATHS


def doUpload(api, uploads, songs):
  for upload in uploads:
    for song in songs:
      if song.md5 == upload:
        print "Uploading ", song, "... ",
        uid = api.upload(song)
        song.uid = uid
        get_db().session.commit()
        print "Done."
        break


def doDownload(api, downloads):
  for download in downloads:
    print "Downloading ", download, "... ",
    song = api.download(download)
    print "Done."
    insert_songs(get_db(), [song])


def doPlaylistSync():
  #TODO: check to see which players are running
  if sys.platform == "darwin":
    from cloudvibe.platform.darwin.wmp import WindowsMediaPlayer
    from cloudvibe.platform.darwin.itunes import ITunesPlayer
  elif sys.platform == "win32":
    from cloudvibe.platform.win32.wmp import WindowsMediaPlayer
    from cloudvibe.platform.win32.itunes import ITunesPlayer

  players = [
      WindowsMediaPlayer()
    , ITunesPlayer()
  ]

  local_playlists = getAllLocalDBPlaylists(get_db())
  
  for i in range(len(players)):
    to_add_to_db, to_add_to_player = players[i].playlistCompare(local_playlists)
    
    for t in range(len(to_add_to_player)):
      songs = getLocalDBPlaylist(get_db(), to_add_to_player[t]).getAllSongNames()
      players[i].createPlaylist(to_add_to_player[t], songs)

    for t in range(len(to_add_to_db)):
      player_songs = players[i].getPlaylistTracks(to_add_to_db[t]) 
      db_songs = get_all_local_songs(get_db())
      songs = []
      for x in range(len(db_songs)):
        if db_songs[x].title in player_songs:
          songs.append(db_songs[x])

      createPlaylist(get_db(), to_add_to_db[t], songs)  

def sync(songs, deleted):
  api = API('bill', 'password')
  downloads, uploads = api.sync(songs)
  print "To Upload:", uploads
  print "To Download:", downloads
  if len(deleted) > 0:
    print "Redownloading deleted songs"
    print deleted
    doDownload(api, deleted)
  doDownload(api, downloads)
  doUpload(api, uploads, songs)
  doPlaylistSync()


def preSync():
  db = get_db()
  dirs = song_dirs()
  files = find_songs(song_dirs())

  songs = []
  for curr_file in files:
    song = Song(curr_file)
    song.load_all()
    songs.append(song)

  to_delete = sync_local_db(get_db(), songs) 

  sync(get_all_local_songs(db), to_delete)

def browse():
  webbrowser.open("http://getcloudvibe.com")

if __name__ == "__main__":
  tray = Tray()
  tray.on('sync', preSync)
  tray.on('site', browse)
  tray.load()

import webbrowser
import cloudvibe.db
from cloudvibe.api import API
from cloudvibe.song import Song, get_all_local_songs, sync_local_db, insert_songs
from cloudvibe.song import song_dirs, find_songs
from cloudvibe.gui import Tray

MONITOR_PATHS = song_dirs()  
DB = cloudvibe.db.get_db()

def get_db():
  return DB

def get_paths():
  return MONITOR_PATHS

def sync(songs):
  api = API('bill', 'password')
  downloads, uploads = api.sync(songs)
  for upload in uploads:
    for song in songs:
      if song.md5 == upload:
        print "Uploading ", song
        api.upload(song)
        break

  print downloads
  for download in downloads:
    print "next"
    api.download('bill', download)

def preSync():
  files = find_songs(MONITOR_PATHS)

  songs = []
  for curr_file in files[2:7]:
    print curr_file
    song = Song(curr_file)
    song.load_all()
    songs.append(song)

  sync(songs)

def browse():
  webbrowser.open("http://getcloudvibe.com")

if __name__ == "__main__":
  tray = Tray()
  tray.on('sync', preSync)
  tray.on('sync', browse)
  tray.load()
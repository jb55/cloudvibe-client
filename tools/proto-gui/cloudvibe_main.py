import cloudvibe.db
from cloudvibe.api import API
from cloudvibe.song import Song, get_all_local_songs, sync_local_db, insert_songs
from cloudvibe.util import GetMusicDirs, GetMusicFiles
from cloudvibe.platform.win_sys_tray_icon import instantiateSysTrayIcon 

MONITOR_PATHS = GetMusicDirs()  
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
        api.upload(song)
        break

  print downloads
  for download in downloads:
    print "next"
    api.download('bill', download)

def preSync():
  files = GetMusicFiles(get_paths())

  songs = []
  for curr_file in files[:150]:
    print curr_file
    song = Song(curr_file)
    song.load_all()
    songs.append(song)

  sync(songs)

if __name__ == "__main__":
  instantiateSysTrayIcon(preSync)

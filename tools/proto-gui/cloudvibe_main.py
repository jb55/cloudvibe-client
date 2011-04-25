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

def doUpload(api, uploads, songs):
  for upload in uploads:
    for song in songs:
      if song.md5 == upload:
        print "Uploading: ", song
        api.upload(song)
        break

def doDownload(api, downloads):
  for download in downloads:
    song = api.download(download)
    insert_songs(get_db(), [song])

def sync(songs):
  api = API('bill', 'password')
  downloads, uploads = api.sync(songs)
  print "To Upload:", uploads
  print "To Download:", downloads
  doDownload(api, downloads)
  doUpload(api, uploads, songs)



def preSync():
  files = find_songs(MONITOR_PATHS)

  songs = []
  for curr_file in files[1:100]:
    song = Song(curr_file)
    song.load_all()
    songs.append(song)

  to_delete = sync_local_db(get_db(), songs) 

  sync(get_all_local_songs(get_db()))

def browse():
  webbrowser.open("http://getcloudvibe.com")

if __name__ == "__main__":
  #preSync()
  tray = Tray()
  tray.on('sync', preSync)
  tray.on('site', browse)
  tray.load()

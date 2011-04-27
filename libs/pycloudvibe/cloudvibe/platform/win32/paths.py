import win32com.client 
import os
from win32com.shell import shell, shellcon

def song_dirs():
  wm = win32com.client.gencache.EnsureDispatch('WMPlayer.OCX')

  songList = []
  try:
    songs = wm.playlistCollection.getByName('All Music')[0]
    for song in songs:
      if ".mp3" in song.sourceURL:
        try:
          songList.append(song.sourceURL)
        except: 
          continue
  except:
    print ""

  songDirList = []
  for song in songList:
    dirPath = song.rsplit('\\')
    dirPathLen = len(dirPath)

    i = 0 
    path = ""
    while i < 2:
      if ".mp3" not in dirPath[i]:
        path += dirPath[i] + "\\"
      i += 1

    if path in songDirList:
      continue

    songDirList.append(path)

  return songDirList


def default_song_dir():
  """ Gets the default music directory """
  common = lambda: shell.SHGetFolderPath(0, shellcon.CSIDL_COMMON_MUSIC, 0, 0)
  user = lambda: shell.SHGetFolderPath(0, shellcon.CSIDL_MYMUSIC, 0, 0)
  return user() or common()

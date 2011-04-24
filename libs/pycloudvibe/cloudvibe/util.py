import os
import config

def init_fs(conf=config.DEFAULT):
  root = conf.get('root')
  if not os.path.exists(root):
    os.mkdir(root)

def intersect(a, b):
  return set(a) & set(b)

def difference(a, b):
  return set(a) ^ set(b)

def GetMusicFiles(dirs):
  files = []
  for dir in dirs:
    for dirpath, dirnames, filenames in os.walk(dir):    
      for filename in [f for f in filenames if f.endswith(".mp3")]:        
        files.append(os.path.join(dirpath, filename).encode("utf-8"))         

  return files

def GetMusicDirs():
  import win32com.client 
  
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

def GetDefaultMusicDirs():
  from win32com.shell import shell, shellcon

  common = shell.SHGetFolderPath(0, shellcon.CSIDL_COMMON_MUSIC, 0, 0)
  user = shell.SHGetFolderPath(0, shellcon.CSIDL_MYMUSIC, 0, 0)
  
  return user or common or "~/.cloudvibe/music"
  

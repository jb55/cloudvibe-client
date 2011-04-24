import json
import os
from net import Http
from settings import SERVER
from song import SongJsonEncoder
from threading import * 
from util import GetDefaultMusicDirs
import urllib2


def genUrl(user, action):
  return SERVER + '/user/' + user + '/' + action

def genS3Url(user, md5):
  return "https://s3.amazonaws.com/cloudvibe/" + user + "/" + md5 + ".mp3"

def encodeSongs(songs):
  encoder = SongJsonEncoder()
  return encoder.encode(songs)

class API():
  " cloudvibe REST api "

  def __init__(self, user, passwd):
    self.user = user
    self.passwd = passwd

  def sync(self, songs):
    http = Http()
    jsn = encodeSongs(songs)
    url = genUrl(self.user, 'sync')
    print url
    res = http.post(url, jsn)
    print res.getcode()
    result = res.read()
    data = json.loads(result)
    return (data["download"], data["upload"])

  def upload(self, song):
    http = Http()
    url = genUrl(self.user, 'upload')
    data = song.toDict()
    file_data = open(song.path)
    data["songFile"] = file_data
    return http.multipart(url, data).read()

  def download(self, user, md5):
    song_dir = GetDefaultMusicDirs()

    url = genS3Url(user, md5)

    file_name = url.split('/')[-1]
    tmp_url = urllib2.urlopen(url)
    path = os.path.join(song_dir, file_name) 
    fp = open(path, 'wb')
    meta = tmp_url.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
      buffer = tmp_url.read(block_sz)
      if not buffer:
        break
      
      file_size_dl += block_sz
      fp.write(buffer)
      status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
      status = status + chr(8)*(len(status)+1)
      print status

    fp.close() 

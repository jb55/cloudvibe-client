import json
from net import Http
from settings import SERVER
from song import SongJsonEncoder
from threading import * 


def genUrl(user, action):
  return SERVER + '/user/' + user + '/' + action

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


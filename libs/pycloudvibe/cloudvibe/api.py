from net import Http
from settings import SERVER
from song import SongJsonEncoder

def genUrl(user, action):
  return SERVER + '/user/' + user + '/' + action

class API():
  " cloudvibe REST api "

  def __init__(self, user, passwd):
    self.user = user
    self.passwd = passwd

  def sync(self, songs):
    http = Http()
    songEncoder = SongJsonEncoder()
    jsn = songEncoder.encode(songs)
    url = genUrl(self.user, 'sync')
    print url
    res = http.post(url, jsn)
    print res.getcode()
    return res.read()
    

import json
import os
from net import Http
from settings import SERVER
from song import SongJsonEncoder, default_song_dir, Song, insert_songs
from threading import * 
import cloudvibe.db
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
    print data
    return (data["download"], data["upload"])


  def upload(self, song):
    http = Http()
    url = genUrl(self.user, 'upload')
    data = song.toDict()
    file_data = open(song.path, 'rb')
    data["songFile"] = file_data
    res = http.multipart(url, data).read()
    return res


  def download(self, uuid):
    http = Http()
    song_dir = default_song_dir()
    url = genUrl(self.user, 'download') + "/" + uuid

    # call our server to get download links and meta data
    res = http.get(url)
    data = json.loads(res.read())

    file_url = data["download_url"]
    file_name = data["filename"]

    path = os.path.join(song_dir, file_name) 
    http.download(file_url, path)

    song = Song(path)

    print "Done downloading", song

    song.load_dict_tags(data)
    song.write_tags()

    return song


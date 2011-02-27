import urllib2
import json
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

# poster init
register_openers()

SERVER = "http://cloudvibe.jb55.com"
USER = "bill"
TEST_DATA = "derp_data"
TEST_JSON = "{\"test\": 1}"

def makeRequest(t, url, data):
  opener = urllib2.build_opener(urllib2.HTTPHandler)
  request = urllib2.Request(url, data)
  request.add_header('Content-Type', 'text/plain')
  request.get_method = lambda: t
  response = opener.open(request)
  return response

def syncUrl(user):
  return SERVER + '/user' + user + '/sync'

class Communicator():
  "Opens a communication channel to cloudvube"

  def __init__(self):
    pass

  def sync(self, user, data):
    return makeRequest('GET', syncUrl(user), data)

  def multipart(self, user, data):
    datagen, headers = multipart_encode(data)
    req = urllib2.Request(syncUrl(user), datagen, headers)
    urllib2.urlopen(req)

  def testSync(self, user=USER, data=TEST_JSON):
    makeRequest('POST', syncUrl(user), data)

  def testPut(self, user=USER, data=TEST_DATA):
    "Test PUT to cloudvibe"
    makeRequest('PUT', SERVER + "/user/" + user, data)

if __name__ == "__main__":
  Communicator().testSync()

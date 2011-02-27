import urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

# poster init
register_openers()

USER = "bill"

def makeRequest(t, url, data):
  opener = urllib2.build_opener(urllib2.HTTPHandler)
  request = urllib2.Request(url, data)
  request.add_header('Content-Type', 'text/plain')
  request.get_method = lambda: t
  response = opener.open(request)
  return response

class Http():
  "Various http helpers"

  def __init__(self):
    pass

  def post(self, url, data):
    return makeRequest('POST', url, data)

  def get(self, url, data):
    return makeRequest('GET', url, data)

  def multipart(self, url, data):
    datagen, headers = multipart_encode(data)
    req = urllib2.Request(url, datagen, headers)
    urllib2.urlopen(req)


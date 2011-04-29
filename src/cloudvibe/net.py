import httplib, mimetypes, urllib2
from MultipartPostHandler import MultipartPostHandler
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

USER = "bill"

def makeRequest(t, url, data):
  opener = urllib2.build_opener(urllib2.HTTPHandler)
  request = None

  if data:
    request = urllib2.Request(url, data)
  else:
    request = urllib2.Request(url)

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

  def get(self, url, data=None):
    return makeRequest('GET', url, data)

  def download(self, url, path):
    tmp_url = urllib2.urlopen(url)
    fp = open(path, 'wb')
    meta = tmp_url.info()
    file_size = int(meta.getheaders("Content-Length")[0])

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

    fp.close()


  def multipart(self, url, fields):
    register_openers()
    datagen, headers = multipart_encode(fields)
    request = urllib2.Request(url, datagen, headers)
    return urllib2.urlopen(request)


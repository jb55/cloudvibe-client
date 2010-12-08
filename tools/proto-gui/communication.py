import urllib2

SERVER = "http://cloudvibe.jb55.com"
USER = "jb55"
TEST_DATA = "derp_data"
TEST_JSON = "{\"test\": 1}"

def makeRequest(t, url, data):
  opener = urllib2.build_opener(urllib2.HTTPHandler)
  request = urllib2.Request(url, data)
  request.add_header('Content-Type', 'text/plain')
  request.get_method = lambda: t
  url = opener.open(request)


class Communicator():
  "Opens a communication channel to cloudvube"

  def __init__(self):
    pass

  def testSync(self, user=USER, data=TEST_JSON):
    makeRequest('POST', SERVER + "/user/" + user + "/sync", data)

  def testPut(self, user=USER, data=TEST_DATA):
    "Test PUT to cloudvibe"
    makeRequest('PUT', SERVER + "/user/" + user, data)

if __name__ == "__main__":
  Communicator().testSync()

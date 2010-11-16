import urllib2

SERVER = "http://cloudvibe.jb55.com"

class Communicator():
  "Opens a communication channel to cloudvube"

  def __init__(self):
    pass

  def testPut(self, user="jb55", data="derp_data"):
    "Test PUT to cloudvibe"
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(SERVER + "/user/" + user, data)
    request.add_header('Content-Type', 'text/plain')
    request.get_method = lambda: 'PUT'
    url = opener.open(request)

if __name__ == "__main__":
  Communicator().testPut()

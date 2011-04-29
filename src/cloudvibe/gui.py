import sys

class Tray():
  """ The Cloudvibe tray """

  def __init__(self):
    self.handlers = {}


  def on(self, event, fn):
    """ 
      Register event handlers 
      
      Events:
        - sync
    """
    if event in self.handlers:
      self.handlers[event].append(fn)
    else:
      self.handlers[event] = [fn]

  def callHandlers(self, event):
    if event in self.handlers:
      for handler in self.handlers[event]:
        handler()

  def onSync(self):
    """ Called when Sync Now is pressed in the tray menu """
    self.callHandlers("sync")

  def onSite(self):
    """ Called when Visit Cloudvibe Website is pressed in the tray menu """
    self.callHandlers("site")

  def getMenu(self):
    return {
      "sync": ("Sync Now", self.onSync),
      "site": ("Visit Cloudvibe Website", self.onSite),
      "quit": ("Quit", None),
    }
    
  def load(self):
    """ Load and start the tray """
    menu = self.getMenu()
    if sys.platform == 'darwin':
      import cloudvibe.platform.darwin.tray as tray
      tray.load(menu)
    elif sys.platform == 'win32':
      import cloudvibe.platform.win32.win_sys_tray_icon as tray
      tray.load(menu)

if __name__ == '__main__':
  tray = Tray()
  def sync():
    print "sync"
  def site():
    print "site"
  tray.on("sync", sync)
  tray.on("site", site)
  tray.load()



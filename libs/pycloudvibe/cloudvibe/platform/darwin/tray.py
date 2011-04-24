import objc
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper

menuDef = None

def callback(event):
  return menuDef[event][1]

def select(event):
  return objc.selector(callback(event), signature='v@:')

def name(event):
  return menuDef[event][0]


class CloudvibeApp(NSApplication):

  def finishLaunching(self):
    # Make statusbar item
    statusbar = NSStatusBar.systemStatusBar()
    self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
    self.icon = NSImage.alloc().initByReferencingFile_('platform/cloudvibe_big.ico')
    self.icon.setScalesWhenResized_(True)
    self.icon.setSize_((20, 20))
    self.statusitem.setImage_(self.icon)

    self.menubarMenu = NSMenu.alloc().init()

    self.syncItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
      name("sync"), "sync:", '')
    self.menubarMenu.addItem_(self.syncItem)

    self.siteItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
      name("site"), "site:", '')
    self.menubarMenu.addItem_(self.siteItem)

    self.quit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
      name("quit"), "terminate:", '')
    self.menubarMenu.addItem_(self.quit)

    #add menu to statusitem
    self.statusitem.setMenu_(self.menubarMenu)
    self.statusitem.setToolTip_('Cloudvibe')

  def sync_(self, n):
    callback("sync")()

  def site_(self, n):
    callback("site")()

def load(menu):
  global menuDef
  menuDef = menu
  app = CloudvibeApp.sharedApplication()
  AppHelper.runEventLoop()


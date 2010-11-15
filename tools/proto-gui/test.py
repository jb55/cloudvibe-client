import wx

class Menu(wx.Frame):
  def __init__(self, parent, id, title):
    wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(200, 150))

    menubar = wx.MenuBar()
    file = wx.Menu()
    edit = wx.Menu()
    help = wx.Menu()

    file.Append(101, '&Open', 'Open a document')
    file.Append(102, '&Save', 'Save the document')
    file.AppendSeparator()
    quit = wx.MenuItem(file, 105, '&Quit\tCtrl+Q', 'Quit the Application')
    file.AppendItem(quit)

    menubar.Append(file, '&File')
    menubar.Append(edit, '&Edit')
    menubar.Append(help, '&Help')
    self.SetMenuBar(menubar)
    self.CreateStatusBar()


class App(wx.App):
  def OnInit(self):
    frame = Menu(None, -1, 'Menu')
    frame.Show()
    return True

app = App(0)
app.MainLoop()

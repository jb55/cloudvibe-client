#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# generated by wxGlade 0.6.3 on Mon Nov 15 10:19:42 2010

import wx
from cloudvibe.api import API
from cloudvibe.song import Song

# begin wxGlade: extracode
# end wxGlade

COLUMNS = {
  "Title": {"id": 0},
  "Artist": {"id": 1},
  "Album": {"id": 2},
}

def syncSongs(songs):
  api = API('bill', 'password')
  downloads, uploads = api.sync(songs)
  for upload in uploads:
    for song in songs:
      if song.md5 == upload:
        api.upload(song)
        break


class FileDropTarget(wx.FileDropTarget):
  """ Implements Drop Target functionality for Files """
  def __init__(self, fn):
    wx.FileDropTarget.__init__(self)
    self.fn = fn

  def OnDropFiles(self, x, y, filenames):
    self.fn(filenames)


class MyDialog(wx.Dialog):
  def __init__(self, *args, **kwds):
    # begin wxGlade: MyDialog.__init__
    kwds["style"] = wx.DEFAULT_DIALOG_STYLE
    wx.Dialog.__init__(self, *args, **kwds)

    self.rightPanel = wx.Panel(self)
    self.songList = wx.ListCtrl(self, -1,
                                style=wx.LC_REPORT|wx.SUNKEN_BORDER)
    self.songId = 1
    self.selectedListItem = None
    self.selectedItemIndex = 0
    self.selectedSong = None

    self.initListCtrl(self.songList)
    self.initRightPanel(self.rightPanel)

    self.addSongButton = wx.Button(self, -1, "Sync")
    self.okButton = wx.Button(self, wx.ID_OK, "")
    self.cancelButton = wx.Button(self, wx.ID_CANCEL, "")

    self.__set_properties()
    self.__do_layout()

    #self.Bind(wx.EVT_LIST_INSERT_ITEM, self.onInsertItem, self.songList)
    self.Bind(wx.EVT_BUTTON, self.onAddSong, self.addSongButton)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onListItemSelected, self.songList)
    self.Bind(wx.EVT_TEXT, self.onArtistChanged, self.txtArtist)
    self.Bind(wx.EVT_TEXT, self.onTitleChanged, self.txtTitle)
    # end wxGlade

  def initListCtrl(self, l):
    l.InsertColumn(0, "Title");
    l.InsertColumn(1, "Artist");
    l.InsertColumn(2, "Album");

    # Add Drop onr
    dropTarget = FileDropTarget(self.onDropFiles)
    l.SetDropTarget(dropTarget)

  def __set_properties(self):
    # begin wxGlade: MyDialog.__set_properties
    self.SetTitle("Song Upload Prototype")
    self.SetSize(wx.DLG_SZE(self, (281, 195)))
    # end wxGlade

  def initRightPanel(self, panel):
    # Make a sizer for our panel
    sizer = wx.BoxSizer(wx.VERTICAL)

    # Text controls
    self.txtArtist = wx.TextCtrl(panel)
    self.txtTitle = wx.TextCtrl(panel)
    self.songs = {}

    pad = wx.BOTTOM | wx.LEFT | wx.EXPAND | wx.RIGHT
    padTop = pad | wx.TOP
    spacing = 7

    staticArtist = wx.StaticText(panel, -1, label="Artist")
    staticTitle = wx.StaticText(panel, -1, label="Title")

    sizer.Add(staticArtist, 0, wx.LEFT | wx.TOP, spacing)
    sizer.Add(self.txtArtist, 0, pad, spacing)
    sizer.Add(staticTitle, 0, wx.LEFT, spacing)
    sizer.Add(self.txtTitle, 0, pad, spacing)
    panel.SetSizer(sizer)
    

  def __do_layout(self):
    # begin wxGlade: MyDialog.__do_layout
    sizer_1 = wx.BoxSizer(wx.VERTICAL)
    sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
    sizer_3 = wx.BoxSizer(wx.HORIZONTAL)

    # Bottom sizer
    sizer_2.Add(self.addSongButton, 0, 0, 0)
    sizer_2.Add(self.okButton, 0, wx.LEFT, 10)
    sizer_2.Add(self.cancelButton, 0, wx.LEFT, 10)

    # Song list / right panel sizer
    sizer_3.Add(self.songList, 2, wx.EXPAND, 10)
    sizer_3.Add(self.rightPanel, 1, wx.EXPAND, 10)

    # Vertically stacked sizer for all other sizers
    sizer_1.Add(sizer_3, 1, wx.EXPAND, 11)
    sizer_1.Add(sizer_2, 0, wx.ALL|wx.ALIGN_RIGHT, 11)

    self.SetSizer(sizer_1)
    self.Layout()
    # end wxGlade

  def onDropFiles(self, files):
    for file in files:
      song = Song(file)
      song.load_all()
      self.addSong(song)

  def addSong(self, song):
    l = self.songList

    ind = l.GetItemCount()
    l.InsertStringItem(ind, song.info["title"] or song.filename)
    item = l.SetStringItem(ind, COLUMNS["Artist"]["id"], song.info["artist"])
    l.SetStringItem(ind, COLUMNS["Album"]["id"], song.info["album"])
    l.SetItemData(ind, self.songId)
    self.songs[self.songId] = song
    self.songId = self.songId + 1

  def onListItemSelected(self, event):
    li = event.GetItem()
    song = self.songs[li.GetData()]
    self.selectedSong = song
    self.selectedListItem = li
    self.selectedItemIndex = event.GetIndex()

    if song.info["artist"]:
      self.txtArtist.SetValue(song.info["artist"])
    else:
      self.txtArtist.Clear()

    if song.info["title"]:
      self.txtTitle.SetValue(song.info["title"])
    else:
      self.txtTitle.Clear()


  def updateListText(self, col, index, s):
    self.songList.SetStringItem(index, col, s)

  def updateListItemArtist(self, index, artist):
    self.updateListText(COLUMNS["Artist"]["id"], index, artist)

  def updateListItemTitle(self, index, title):
    self.updateListText(COLUMNS["Title"]["id"], index, title)

  def onArtistChanged(self, event):
    if self.selectedListItem:
      artist = event.GetString()
      self.updateListItemArtist(self.selectedItemIndex, artist)
      self.selectedSong.artist = artist

  def onTitleChanged(self, event):
    if self.selectedListItem:
      title = event.GetString()
      self.updateListItemTitle(self.selectedItemIndex, title)
      self.selectedSong.title = title

  def onAddSong(self, event): # wxGlade: MyDialog.<event_onr>
    syncSongs(self.songs.values())
    

# end of class MyDialog


if __name__ == "__main__":
  app = wx.PySimpleApp(0)
  wx.InitAllImageHandlers()
  dialog_1 = MyDialog(None, -1, "")
  app.SetTopWindow(dialog_1)
  dialog_1.Show()
  app.MainLoop()

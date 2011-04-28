import win32com.client

class WindowsMediaPlayer:
  def __init__(self):
    pass

  def getWMP(self):
    return win32com.client.gencache.EnsureDispatch('WMPlayer.OCX')

  def getPlaylists(self):
    wmp = self.getWMP()
    playlists = []
    pl_tmp = wmp.playlistCollection.getAll()
    for i in range(pl_tmp.count):
      playlists.append(pl_tmp[i].name)

    wmp.close()

    return playlists

  def getPlaylistTracks(self, playlist):
    wmp = self.getWMP()
    tracks = []
    pl_tmp = wmp.playlistCollection.getByName(playlist)
    for i in range(pl_tmp.Item(0).count):
      tracks.append(pl_tmp.Item(0)[i].name)

    wmp.close()

    return tracks

  def createPlaylist(self, pl_name, songs=[]):
    wmp = self.getWMP()
    playlist = wmp.playlistCollection.newPlaylist(pl_name)
    
    if len(songs) > 0:
      all_songs = wmp.playlistCollection.getByName('All Music').Item(0)
      wmp.close()

      for i in range(all_songs.count):
        if all_songs[i].name in songs:
          self.addPlaylistTrack(all_songs[i], pl_name)
      return
    
    wmp.close()

  def addPlaylistTrack(self, song, pl_name):
    wmp = self.getWMP()
    # TODO: There is an issue here with encoding and getting a playlist by name
    playlist = wmp.playlistCollection.getByName(pl_name.encode("utf-8")).Item(0)
    playlist.appendItem(song)
    wmp.close()

  def deletePlaylist(self, pl_name):
    wmp = self.getWMP()
    playlist = wmp.playlistCollection.getByName(pl_name).Item(0)
    wmp.playlistCollection.remove(playlist)
    wmp.close()

  def removePlaylistTracks(self, pl_name, songs=[]):
    wmp = self.getWMP()
    playlist = wmp.playlistCollection.getByName(pl_name).Item(0)
    
    if len(songs) > 0:
      all_songs = wmp.playlistCollection.getByNames('All Music').Item(0)

      for i in range(all_songs.count):
        if all_songs[i].name in songs:
          playlist.removeItem(all_songs[i])

    wmp.close()

  def playlistCompare(self, to_compare_playlists):
    wmp_playlists = self.getPlaylists()

    wmp_playlists_missing = []
    to_compare_playlists_missing = []
    for i in range(len(wmp_playlists)):
      if wmp_playlists[i] not in to_compare_playlists:
        to_compare_playlists_missing.append(wmp_playlists[i]) 

    for i in range(len(to_compare_playlists)):
      if to_compare_playlists[i] not in wmp_playlists:
        wmp_playlists_missing.append(to_compare_playlists[i]) 

    return to_compare_playlists_missing, wmp_playlists_missing

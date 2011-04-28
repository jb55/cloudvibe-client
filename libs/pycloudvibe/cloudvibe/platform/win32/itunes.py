import win32com.client

class ITunesPlayer:
  def __init__(self):
    pass

  def getITP(self):
    return win32com.client.gencache.EnsureDispatch('iTunes.Application')

  def getPlaylists(self, ):
    itp = self.getITP()
    playlists = []
    pl_tmp = itp.LibrarySource.Playlists
    for i in range(pl_tmp.Count):
      playlists.append(pl_tmp[i].Name)

    return playlists

  def getPlaylistTracks(self, playlist):
    itp = self.getITP()
    tracks = []
    pl_tmp = itp.LibrarySource.Playlists.ItemByName(playlist).Tracks
    for i in range(pl_tmp.Count):
      tracks.append(pl_tmp[i].Name)

    return tracks

  def createPlaylist(self, pl_name, songs=[]):
    itp = self.getITP()
    playlist = itp.CreatePlaylist(pl_name)
    
    if len(songs) > 0:
      all_songs = itp.LibraryPlaylist.Tracks

      for i in range(all_songs.Count):
        if all_songs[i].Name in songs:
          self.addPlaylistTrack(all_songs[i], pl_name)
      return
    
  def addPlaylistTrack(self, song, pl_name):
    itp = self.getITP()
    playlist = itp.LibrarySource.Playlists.ItemByName(pl_name)
    playlist = win32com.client.CastTo(playlist, 'IITUserPlaylist')
    playlist.AddTrack(song)

  def deletePlaylist(self, pl_name):
    itp = self.getITP()
    playlist = itp.LibrarySource.Playlists.ItemByName(pl_name)
    playlist.Delete()

  def removePlaylistTracks(self, pl_name, songs=[]):
    pass

  def playlistCompare(self, to_compare_playlists):
    itp_playlists = self.getPlaylists()

    itp_playlists_missing = []
    to_compare_playlists_missing = []
    for i in range(len(itp_playlists)):
      if itp_playlists[i] not in to_compare_playlists:
        to_compare_playlists_missing.append(itp_playlists[i]) 

    for i in range(len(to_compare_playlists)):
      if to_compare_playlists[i] not in itp_playlists:
        itp_playlists_missing.append(to_compare_playlists[i]) 

    return to_compare_playlists_missing, itp_playlists_missing

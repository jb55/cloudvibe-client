import win32com.client

class ITunesPlayer:
  def __init__(self):
    pass

  def getITP():
    return win32com.client.gencache.EnsureDispatch('iTunes.Application')

  def getPlaylists():
    itp = getITP()
    playlists = []
    pl_tmp = itp.LibrarySource.Playlists
    for i in range(pl_tmp.Count):
      playlists.append(pl_tmp[i].Name)

    itp.close()

    return playlists

  def getPlaylistTracks(playlist):
    itp = getITP()
    tracks = []
    pl_tmp = itp.LibrarySource.Playlists.ItemByName(playlist).Tracks
    for i in range(pl_tmp.Count):
      tracks.append(pl_tmp[i].Name)

    itp.close()

    return tracks

  def createPlaylist(pl_name, songs=[]):
    itp = getITP()
    playlist = itp.CreatePlaylist(pl_name)
    
    if len(songs) > 0:
      all_songs = itp.LibraryPlaylist.Tracks
      itp.close()

      for i in range(all_songs.Count):
        if all_songs[i].Name in songs:
          addPlaylistTrack(all_songs[i], pl_name)
      return
    
    itp.close()

  def addPlaylistTrack(song, pl_name):
    itp = getITP()
    playlist = itp.LibrarySource.Playlists.ItemByName(pl_name)
    playlist = win32com.client.CastTo(playlist, 'IITUserPlaylist')
    playlist.AddTrack(song)
    itp.close()

  def deletePlaylist(pl_name):
    itp = getITP()
    playlist = itp.LibrarySource.Playlists.ItemByName(pl_name)
    playlist.Delete()
    itp.close()

  def removePlaylistTracks(pl_name, songs=[]):
    pass

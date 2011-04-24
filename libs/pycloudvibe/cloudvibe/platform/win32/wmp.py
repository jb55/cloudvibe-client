import win32com.client

class WindowsMediaPlayer:
  def __init__(self):
    pass

  def getWMP():
    return win32com.client.gencache.EnsureDispatch('WMPlayer.OCX')

  def getPlaylists():
    wmp = getWMP()
    playlists = []
    pl_tmp = wmp.playlistCollection.getAll()
    for i in range(pl_tmp.count):
      playlists.append(pl_tmp[i].name)

    wmp.close()

    return playlists

  def getPlaylistTracks(playlist):
    wmp = getWMP()
    tracks = []
    pl_tmp = wmp.playlistCollection.getByName(playlist)
    for i in range(pl_tmp.Item(0).count):
      tracks.append(pl_tmp.Item(0)[i].name)

    wmp.close()

    return tracks

  def createPlaylist(pl_name, songs=[]):
    wmp = getWMP()
    playlist = wmp.playlistCollection.newPlaylist(pl_name)
    
    if len(songs) > 0:
      all_songs = wmp.playlistCollection.getByName('All Music').Item(0)
      wmp.close()

      for i in range(all_songs.count):
        if all_songs[i].name in songs:
          addPlaylistTrack(all_songs[i], pl_name)
      return
    
    wmp.close()

  def addPlaylistTrack(song, pl_name):
    wmp = getWMP()
    playlist = wmp.playlistCollection.getByName(pl_name).Item(0)
    playlist.appendItem(song)
    wmp.close()

  def deletePlaylist(pl_name):
    wmp = getWMP()
    playlist = wmp.playlistCollection.getByName(pl_name).Item(0)
    wmp.playlistCollection.remove(playlist)
    wmp.close()

  def removePlaylistTracks(pl_name, songs=[]):
    wmp = getWMP()
    playlist = wmp.playlistCollection.getByName(pl_name).Item(0)
    
    if len(songs) > 0:
      all_songs = wmp.playlistCollection.getByNames('All Music').Item(0)

      for i in range(all_songs.count):
        if all_songs[i].name in songs:
          playlist.removeItem(all_songs[i])

    wmp.close()

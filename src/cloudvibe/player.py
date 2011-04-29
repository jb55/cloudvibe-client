class Player:
  WMP = False
  ITUNES = False

  def __init__(self, player_type):
    if player_type == "WMP":
      WMP = True
    elif player_type == "ITUNES":
      ITUNES = True

  def getPlaylists():
    if sys.platform == 'darwin':
      import cloudvibe.platform.darwin.wmp as wmp
    elif sys.platform == 'win32':
      import cloudvibe.platform.win32.wmp as wmp

  def getPlaylistTracks(pl_name):

  def createPlaylist(pl_name, songs): 

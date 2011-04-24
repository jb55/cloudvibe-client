import os

DEFAULT = os.path.expanduser("~/Music")

def song_dirs():
  return [default_song_dir()]

def default_song_dir():
  return DEFAULT


import os

class Config():
  def __init__(self):
    self.d = {}
  
  def get(self, k):
    return self.d[k]
    
  def set(self, k, v):
    self.d[k] = v


def default_root_path():
  p = os.path.expanduser('~')
  return os.path.join(p, ".cloudvibe")


def default_config():
  c = Config()

  root_path = default_root_path()
  db_file = os.path.join(root_path, 'storage.db')

  c.set('root', root_path)
  c.set('db_file', db_file)
  c.set('db_engine', "sqlite:///" + db_file)

  return c

DEFAULT = default_config()


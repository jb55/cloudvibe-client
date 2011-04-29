import os
import config
import sys

def init_fs(conf=config.DEFAULT):
  root = conf.get('root')
  if not os.path.exists(root):
    os.mkdir(root)

def intersect(a, b):
  return set(a) & set(b)

def difference(a, b):
  return set(a) ^ set(b)

def ensure_path(p):
  if not os.path.exists(p):
    os.mkdir(p)

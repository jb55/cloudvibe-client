
from sqlalchemy import *
import config
import os
import util


def get_db(conf=config.DEFAULT):
  util.init_fs(conf)
  engine = conf.get('db_engine')
  db = create_engine(engine)
  return db



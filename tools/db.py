# connect to the database
from __future__ import print_function
import os
#import psycopg2
#import urllib.parse as urlparse
import urlparse
import sys

def perr(s):
  print(s, file=sys.stderr)

urlparse.uses_netloc.append("postgres")
#url = urlparse.urlparse(os.environ["HEROKU_POSTGRESQL_ORANGE_URL"])
url = urlparse.urlparse("http://a:b@localhost:123/path")

class DB2DIR:
  def __init__(self):
    self.type = 'dir'

  def connect(self, database, user, password, host, port):
    self.database = database
    self.user = user
    self.password = password
    self.host = host
    self.port = port

  def cursor(self):
    self._cursor = 0
    return self

  def execute(self, *args):
    if args[0] == "SELECT name, data FROM data OFFSET floor(random() * (SELECT count(*) FROM data)) LIMIT 1":
      return self.random_image()
    elif args[0].find('SELECT') > -1:
      return self.get_mask(args[1])
    elif args[0][:11]=="INSERT into":
      cmd = args[1]
      return self.insert(cmd)

  def get_mask(self, f):
    self._data = [[file('mask/'+f[0]).read()]]
    self._cursor = 0

  def insert(self, cmd):
    f = cmd
    name = f[0].strip()
    data = f[1].strip()
    file('mask/'+name,'w').write(data)

  def commit(self):
    self.cmd = 'commit'
  def close(self):
    self.cmd = 'close'

  def fetchone(self):
    i = self._cursor
    self._cursor += 1
    return self._data[i]

  def random_image(self):
    name = '001.jpg.b64'
    self._data = [(name, file('orig/'+name).read())]

  def _encode(self, f):
    dat = "data:image/png;base64,"+base64.b64encode(open(f).read())

conn = DB2DIR()
perr(url)
conn.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)


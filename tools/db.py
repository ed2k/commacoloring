# connect to the database
import os
#import psycopg2
import urllib.parse as urlparse

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
    if len(args) == 1: cmd = args[0]
    elif len(args) == 2: cmd = args[0].format(args[1])
    if cmd == "SELECT name, data FROM data OFFSET floor(random() * (SELECT count(*) FROM data)) LIMIT 1":
      return self.random_image()
    elif cmd[:11]=="INSERT into":
      idx = cmd.find('VALUES (')
      return self.insert(cmd[idx+8:-1])

  def insert(self, cmd):
    f = cmd.split(',')
    print(f)
    name = f[0].strip()
    data = f[1].strip()
    track = f[2].strip()
    email = f[3].strip()
    gid = f[4].strip()

  def commit(self):
    self.commit = 1
  def close(self):
    self.close = 1

  def fetchone(self):
    name,data = (self._data[self._cursor])
    self._cursor += 1
    return (name, data)

  def random_image(self):
    name = '001.jpg.b64'
    self._data = [(name, file(name).read())]

  def _encode(self, f):
    dat = "data:image/png;base64,"+base64.b64encode(open(f).read())

conn = DB2DIR()
print (url)
conn.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)


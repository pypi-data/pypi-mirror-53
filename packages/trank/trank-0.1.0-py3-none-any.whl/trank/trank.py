#
# Copyright (c) 2019, Grupo Investigativo de Sistemas
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# 
import os
import urllib.parse
import json
import flask
from flask import url_for
import psycopg2
import psycopg2.extensions
from psycopg2.extras import Json
from queuepool.pool import Pool
from queuepool.psycopg2cm import ConnectionManagerExtended
from trank import __version__ as trank_version
import threading
import collections
import pyaconf


config = pyaconf.load(os.environ['TRANK_CONFIG'])


BASE = config['prefix']
PFX = config['core_path']
FULLPFX = BASE + PFX


dbpoolConf = config['dbpool']
dbpool = Pool(
   name = dbpoolConf['name'],
   capacity = dbpoolConf['capacity'],
   maxIdleTime = dbpoolConf['max_idle_time'],
   maxOpenTime = dbpoolConf['max_open_time'],
   maxUsageCount = dbpoolConf['max_usage_count'],
   closeOnException = dbpoolConf['close_on_exception'],
)
for i in range(dbpool.capacity):
   dbpool.put(ConnectionManagerExtended(
      name = dbpool.name + '-' + str(i),
      autocommit = False,
      isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
      dbname = dbpool.name,
      host = dbpoolConf['host'],
      user = dbpoolConf['user'],
      password = dbpoolConf['password'],
   ))
if dbpoolConf['recycle_interval'] is not None:
   dbpool.startRecycler(dbpoolConf['recycle_interval'])


#------------------------------------


app = flask.Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')


def build_url(location, base=BASE, params={}):
   s = ""
   for k,v in params.items():
      s += ("?" if len(s)==0 else "&") + k + "=" + (urllib.parse.quote(str(v)) if v is not None else "")
   return (location[0]=='/' and base or '') + location + s
   

def rredirect(location, code=302, Response=None, base=BASE, params={}):
   s = build_url(location, base, params)
   return flask.redirect(s, code, Response)


def jsonify(data, status=200):
   return flask.Response( response=json.dumps(data), status=status, mimetype='application/json')


# ---


@app.route(f'{PFX}')
def index():
   """ Index page displays "Hello, world!"
   """
   return flask.render_template('hello.jade', PFX=PFX, FULLPFX=FULLPFX)


@app.route(f'/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route(f'{PFX}/images/<path:path>')
def imagepath(path):
    return app.send_static_file(path)


@app.route(f'{PFX}/players')
def players():
   """ An endpoint that returns the list of players in json format
   """
   with dbpool.take() as cm:
      with cm.resource: # transaction
         rs = cm.query("select player_id, phone, full_name, email from players order by player_id;")

   return jsonify(dict(players=rs))


@app.route(f'{PFX}/info')
def processInfo():
   return jsonify(dict(
      version=trank_version,
      pid=os.getpid(),
      active_count=threading.active_count(),
      current_thread_name=threading.current_thread().name,
      ident=threading.get_ident(),
      main_thread_ident=threading.main_thread().ident,
      stack_size=threading.stack_size(),
      threads={ x.ident: dict(name=x.name, is_alive=x.is_alive(), is_daemon=x.daemon) for x in threading.enumerate() },
   ))


# ------------------


def start():
   flaskConf = config['flask']
   app.run(
      host=flaskConf['host'],
      port=flaskConf['port'],
      debug = flaskConf['debug'],
      threaded=flaskConf['threaded'],
      processes=flaskConf['processes'],
      ssl_context=(flaskConf['ssl_cert'],flaskConf['ssl_key']),
   )

if __name__ == '__main__':
   start()

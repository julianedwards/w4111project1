#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following uses the sqlite3 database test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111db.eastus.cloudapp.azure.com/username
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@w4111db.eastus.cloudapp.azure.com/ewu2493"
#
DATABASEURI = "postgresql://jse2122:CHUNGY@w4111db.eastus.cloudapp.azure.com/jse2122"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args

  interest_cursor = g.conn.execute("SELECT * FROM Interests") 
  interests = []
  for result in interest_cursor:
      interests.append(result)
  interest_cursor.close()

  zip_cursor = g.conn.execute("SELECT DISTINCT zip_code FROM Groups")
  zip_codes = []
  for result in zip_cursor:
      zip_codes.append(result[0])
  zip_cursor.close()
  strzips = []
  for z in zip_codes:
      strzips.append(str(z))

  # inside groups
  user_cursor = g.conn.execute("SELECT name FROM Users")
  users = []
  for result in user_cursor:
      users.append(result)
  user_cursor.close()

  interest = request.args.get("interest")
  if interest == "All":
      interest = None 
  zip_code = request.args.get("zip_code")
  if zip_code == "All":
      zip_code = None 
  user = request.args.get("user")
  if user == "All":
      user = None 

  results = []
  if interest and zip_code and user:
      result_cursor = g.conn.execute("SELECT g.name, g.content, g.level, "+
              "g.zip_code, g.type FROM Groups g, Joined j, Users u WHERE " + 
              "g.type =\'"+ interest + "\' AND g.zip_code=\'"+ zip_code +
              "\' AND u.name=\'" + user + "\' AND u.uid=j.uid AND j.gid=g.gid")
      for result in result_cursor:
          results.append(result)
      result_cursor.close()

  elif zip_code and user:
      result_cursor = g.conn.execute("SELECT g.name, g.content, g.level, " +
              "g.zip_code, g.type FROM Groups g, Joined j, Users u WHERE " +
              "u.name=\'" + user + "\' AND g.zip_code=\'" + zip_code + "\'" + 
              "AND u.uid=j.uid AND j.gid=g.gid")
      for result in result_cursor:
          results.append(result)
      result_cursor.close()

  elif interest and zip_code:
      result_cursor = g.conn.execute("SELECT g.name, g.content, g.level, " +
              "g.zip_code, g.type FROM Groups g WHERE g.type =\'" + interest + 
              "\' AND g.zip_code =\'" + zip_code + "\'")
      for result in result_cursor:
          results.append(result)
      result_cursor.close()

  elif interest and user:
      result_cursor = g.conn.execute("SELECT g.name, g.content, g.level, " +
              "g.zip_code, g.type FROM Groups g, Joined j, Users u WHERE " +
              "g.type =\'" + interest + "\' AND u.name =\'" + user + "\' " +
              "AND u.uid=j.uid AND j.gid=g.gid")
      for result in result_cursor:
          results.append(result)
      result_cursor.close()

  elif interest:
      result_cursor = g.conn.execute("SELECT g.name, g.content, g.level, " +
              "g.zip_code, g.type FROM Groups g WHERE g.type=\'" + interest + 
              "\'")
      for result in result_cursor:
          results.append(result)
      result_cursor.close()

  elif zip_code:
      result_cursor = g.conn.execute("SELECT g.name, g.content, g.level, " +
              "g.zip_code, g.type FROM Groups g WHERE g.zip_code=\'" + 
              zip_code + "\'")
      for result in result_cursor:
          results.append(result)
      result_cursor.close()

  elif user:
      result_cursor = g.conn.execute("SELECT g.name, g.content, g.level, " +
              "g.zip_code, g.type FROM Groups g, Joined j, Users u WHERE " +
              "u.name=\'" + user + "\' AND u.uid=j.uid AND j.gid=g.gid")
      for result in result_cursor:
          results.append(result)
      result_cursor.close()
 
  else:
      result_cursor = g.conn.execute("SELECT g.name, g.content, g.level, " +
              "g.zip_code, g.type FROM groups g")
      for result in result_cursor:
          results.append(result)
      result_cursor.close()

  names = {} 
  for result in results:
      name_cursor = g.conn.execute("SELECT u.name, u.sex, u.age, " +
              "u.zip_code FROM Users u, Joined j, Groups g WHERE g.name=\'" + 
              result[0] + "\' AND j.gid=g.gid AND u.uid=j.uid")
      names[result[0]] = []
      for name in name_cursor:
          names[result[0]].append(name)
      name_cursor.close()
  
  # outside groups
  ointerest = request.args.get("ointerest")
  if ointerest == "All":
      ointerest = None 
  ozip_code = request.args.get("ozip_code")
  if ozip_code == "All":
      ozip_code = None 

  oresults = []
  if ointerest and ozip_code:
      result_cursor = g.conn.execute("SELECT * FROM Outside_Groups o WHERE " + 
              "o.type=\'" + ointerest + "\' AND o.zip_code=\'" + ozip_code + 
              "\'")
      for result in result_cursor:
          oresults.append(result)
      result_cursor.close()

  elif ointerest:
      result_cursor = g.conn.execute("SELECT * FROM Outside_Groups " +
              "o WHERE o.type =\'" + ointerest + "\'")
      for result in result_cursor:
          oresults.append(result)
      result_cursor.close()

  elif ozip_code:
      result_cursor = g.conn.execute("SELECT * FROM Outside_Groups " +
              "o WHERE o.zip_code=\'" + ozip_code + "\'")
      for result in result_cursor:
          oresults.append(result)
      result_cursor.close()


  else:
      result_cursor = g.conn.execute("SELECT * FROM Outside_Groups")
      for result in result_cursor:
          oresults.append(result)
      result_cursor.close()
 
  #friends
  friend = request.args.get("friend")

  friends = []
  if friend != "Choose" and friend != None:
      uid = ""
      uid_cursor = g.conn.execute("SELECT u.uid FROM Users u WHERE u.name=\'" + friend + "\'")
      for u in uid_cursor:
          uid = u[0]
      friend_cursor = g.conn.execute("SELECT u.name FROM Users u WHERE " +
              "u.uid IN (SELECT uid FROM (SELECT f.uid2 as uid FROM Friend " +
              "f WHERE f.uid1=\'" + uid + "\' UNION SELECT f2.uid1 FROM " +
              "Friend f2 WHERE f2.uid2=\'" + uid + "\') AS s)")
      for f in friend_cursor:
          print f
          friends.append(f) 
  # events
  events = []
  event_cursor = g.conn.execute("SELECT * FROM Events")
  for event in event_cursor:
      events.append(event)
  result_cursor.close()

  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  
  return render_template("index.html", interests=interests,
          zip_codes=strzips, users=users, chosen_interest=interest, 
          chosen_zip=zip_code, chosen_user=user, results=results,
          names = names, ochosen_interest=ointerest, ochosen_zip=ozip_code,
          oresults = oresults, fchosen_user=friend, friends=friends, 
          events=events)

#
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()

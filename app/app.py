'''
coral - a Python/Mongo blog using Flask, a web frameworks.
6-18-14
ryan@ryanhartje.com
http://github.com/ryanhartje/coral/

Please report any bugs at:
  https://github.com/RyanHartje/coral/issues/new
'''

from flask import Flask, render_template, request, redirect, url_for
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from wtforms import StringField,RadioField,SelectField,TextAreaField,SubmitField
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

app = Flask(__name__)
Bootstrap(app)

# Instanciate our variables for date and also for mongo here
date = datetime.datetime.now()
client = MongoClient()
db = client.coral
session = {'logged_in':False}
i = datetime.datetime.now()

def settings():
  return db.settings.find_one({'name':'settings'})

def sidebar():
  return db.settings.find_one({'name':'sidebar'})

@app.route('/')
def index():

  # Sort our posts decending from latest to eldest
  #     This does not raise an error if posts is blank so no catch is necessary
  posts = db.posts.find().sort('date',-1)

  # Try to grab our sidebar
  try:
    sidebar = db.settings.find_one({'name':'sidebar'})
    settings = db.settings.find_one({'name':'settings'})
  except:
    sidebar = {'sidebar':''}
    settings = {'title':'Coral'}

  return render_template('index.html',blog_title=settings()['title'],posts=posts,keywords="austindevlabs, free python hosting, python interpreter",logged_in=session['logged_in'],sidebar=sidebar)

@app.route('/view/<postid>')
def view(postid):
  post = db.posts.find_one({'_id':ObjectId(postid)})
  print(post)
  try:
    keywords=post['keywords']
  except:
    keywords=""

  # Try to grab our sidebar
  try:
    sidebar = db.settings.find_one({'name':'sidebar'})
    settings = db.settings.find_one({'name':'settings'})
  except:
    sidebar = {'sidebar':''}
    settings = {'title':'Coral'}

  return render_template('view.html',blog_title="Bug Blog",post=post,keywords=keywords,logged_in=session['logged_in'],sidebar=sidebar)

@app.route('/add/',methods=['GET','POST'])
def add():
  if request.method=='GET':
    return render_template('badd.html',blog_title="Bug Blog",logged_in=session['logged_in'])
  elif request.method=='POST':
    title = request.form['title']
    body = request.form['body']#.replace('\r\n','<br />')
    keywords = request.form['keywords']
    #try:
    db.posts.insert({'date':i,'title':title,'body':body,'keywords':keywords})
    #except: 
    #  return render_template('uhoh.html')

  # Try to grab our sidebar
  try:
    sidebar = db.settings.find_one({'name':'sidebar'})
    settings = db.settings.find_one({'name':'settings'})
  except:
    sidebar = {'sidebar':''}
    settings = {'title':'Coral'}



    return redirect(url_for('index',blog_title="Bug Blog",sidebar=sidebar,logged_in=session['logged_in']))

@app.route('/edit/<post_id>',methods=['GET'])
def edit(post_id):
  post=db.posts.find_one({'_id':ObjectId(post_id)})
  return render_template('edit.html',blog_title="Bug Blog",post=post,logged_in=session['logged_in'])

@app.route('/edit/',methods=['POST'])
def pedit():
  title = request.form['title']
  body = request.form['body']#.replace('\r\n','<br />')
  keywords = request.form['keywords']
  #try:
  print(db.posts.update({'_id':ObjectId(request.form['post_id'])},{'date':i,'title':title,'body':body,'keywords':keywords},safe=False,upsert=False))
  #except: 
  #  return render_template('uhoh.html')
  posts=db.posts.find()
  return redirect(url_for('index',blog_title="Bug Blog",posts=posts,logged_in=session['logged_in']))

@app.route('/remove/<post_id>',methods=['GET'])
def remove(post_id):
  title = db.posts.find_one({'_id':ObjectId(post_id)})
  print(db.posts.remove({'_id':ObjectId(post_id)}))
  return render_template('remove.html',blog_title="Bug Blog",title=title)

@app.route('/login/',methods=['GET','POST'])
def login():
  if request.method=='GET':
    return render_template('login.html',blog_title="Bug Blog",logged_in=session['logged_in'])

  elif request.method=='POST':
    posts = db.posts.find()
    user = request.form['username']
    if user == "ryan":
      if request.form['password']=="coral":
        session['logged_in'] = True
        print("\n\nRyan Logged in\n\n")
      else:
        session['logged_in'] = False
    else:
      session['logged_in'] = False
    return redirect(url_for('index',blog_title="Bug Blog",posts=posts,logged_in=session['logged_in']))

@app.route('/logout/')
def logout():
  #session.pop('logged_in', None)
  session['logged_in']=False
  print("You've been logged out")
  return redirect (url_for('index'))

@app.route('/vote/', methods=['POST'])
def vote():
  # If score exists let's update it else instanciate it at 1 or -1
  data = request.json
  print(db.posts.update({'_id':ObjectId(request.json['_id'])},{vote: request.json['vote']},safe=False,upsert=False))

@app.route('/settings/', methods=['GET','POST'])
def settings():
  if request.method=='GET':
    try:
      settings = db.settings.find_one({'name':'settings'})
      return render_template('settings.html',settings=settings,logged_in=session['logged_in'])
    except:
      return render_template('settings.html',blog_title="Coral",logged_in=session['logged_in'])

  else:
    print("locating any prior settings")
    settings = db.settings.find_one({'name':'settings'})      
    if settings is None:
      #print("attempting to insert settings: " + request.form)
      print("Inserting new settings")
      db.settings.insert({'name':'settings','title':request.form['title'],'logo':request.form['logo'],'comments':request.form['comments'],'perpage':request.form['perpage'],'gcode':request.form['gcode'],'keywords':request.form['keywords']})
    else:
      print("Updating current settings")
      db.settings.update({'_id':ObjectId(settings['_id'])},{'name':'settings','title':request.form['title'],'logo':request.form['logo'],'comments':request.form['comments'],'perpage':request.form['perpage'],'gcode':request.form['gcode'],'keywords':request.form['keywords']},upsert=False,safe=False)
      settings = db.settings.find_one({'name':'settings'})      
    
    print(settings)
    return redirect(url_for('index',blog_title=settings['title'],logged_in=session['logged_in']))

@app.route('/settings/sidebar/', methods=['GET','POST'])
def sidebar():
  
  try:
    sidebar = db.settings.find_one({'name':'sidebar'})
    print("Got Sidebar: " + sidebar['sidebar'])
  except:
    sidebar = {}
    print("Sidebar undefinied")
  
  if request.method=='GET':
    return render_template('sidebar.html',blog_title="Bug Blog",logged_in=session['logged_in'],sidebar=sidebar)

  elif request.method=='POST':
    sidebar = db.settings.find_one({'name':'sidebar'})
    user_input = request.form['sidebar']
    try:
      db.settings.update({'_id':ObjectId(sidebar['_id'])},{'name':'sidebar','sidebar':user_input},safe=False,upsert=False)
      print("Updating sidebar")
    except:
      db.settings.insert({'name':'sidebar','sidebar':user_input})
      print("Exception Thrown, inserting sidebar")
      #print(db.settings.find_one({'name':'sidebar'}))

    posts = db.posts.find()
    return redirect(url_for('index',blog_title="Bug Blog",logged_in=session['logged_in'],posts=posts))
 

if __name__ == "__main__":
  app.run(host="0.0.0.0",debug=True)

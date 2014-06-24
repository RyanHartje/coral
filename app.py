'''
coral - a Python/Mongo blog using Flask, a web frameworks.
6-18-14
ryan@ryanhartje.com
http://github.com/ryanhartje

pre alpha

Functions:
  create post
  delete post
  edit post
  view posts
  view all posts
'''

from flask import Flask, render_template, request, redirect, url_for
from flask.ext.bootstrap import Bootstrap
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import settings

app = Flask(__name__)
Bootstrap(app)

# Instanciate our variables for date and also for mongo here
date = datetime.datetime.now()
client = MongoClient()
db = client.coral
session = {}
session['logged_in']=False
i = datetime.datetime.now()

@app.route('/')
def index():
  posts = db.posts.find()
  return render_template('index.html',blog_title=settings.blog_title,posts=posts,keywords="austindevlabs, free python hosting, python interpreter",logged_in=session['logged_in'])

@app.route('/add/',methods=['GET','POST'])
def add():
  if request.method=='GET':
    return render_template('badd.html',blog_title=settings.blog_title,logged_in=session['logged_in'])
  elif request.method=='POST':
    title = request.form['title']
    body = request.form['body']#.replace('\r\n','<br />')
    #try:
    db.posts.insert({'date':i,'title':title,'body':body})
    #except: 
    #  return render_template('uhoh.html')
    return render_template('index.html',blog_title=settings.blog_title,logged_in=session['logged_in'])

@app.route('/edit/<post_id>',methods=['GET'])
def edit(post_id):
  post=db.posts.find_one({'_id':ObjectId(post_id)})
  return render_template('edit.html',blog_title=settings.blog_title,post=post,logged_in=session['logged_in'])

@app.route('/edit/',methods=['POST'])
def pedit():
  title = request.form['title']
  body = request.form['body']#.replace('\r\n','<br />')
  #try:
  print(db.posts.update({'_id':ObjectId(request.form['post_id'])},{'date':i,'title':title,'body':body},safe=False,upsert=False))
  #except: 
  #  return render_template('uhoh.html')
  return redirect(url_for('index.html',blog_title=settings.blog_title,logged_in=session['logged_in']))

@app.route('/remove/<post_id>',methods=['GET'])
def remove(post_id):
  title = db.posts.find_one({'_id':ObjectId(post_id)})
  print(db.posts.remove({'_id':ObjectId(post_id)}))
  return render_template('remove.html',blog_title=settings.blog_title,title=title)

@app.route('/login/',methods=['GET','POST'])
def login():
  if request.method=='GET':
    return render_template('login.html',blog_title=settings.blog_title,logged_in=session['logged_in'])

  elif request.method=='POST':
    user = request.form['username']
    if user == "ryan":
      if request.form['password']=="coral":
        session['logged_in'] = True
        print("\n\nRyan Logged in\n\n")
      else:
        session['logged_in'] = False
    else:
      session['logged_in'] = False
    return redirect(url_for('index',blog_title=settings.blog_title,logged_in=session['logged_in']))

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

 

if __name__ == "__main__":
  app.run(debug=True)

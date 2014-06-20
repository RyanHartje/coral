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

from flask import Flask, render_template, request
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
i = datetime.datetime.now()

@app.route('/')
def index():
  posts = db.posts.find()
  return render_template('index.html',blog_title=settings.blog_title,posts=posts)

@app.route('/add/',methods=['GET'])
def add():
  return render_template('badd.html',blog_title=settings.blog_title)

@app.route('/add/',methods=['POST'])
def nadd():
  title = request.form['title']
  body = request.form['body']#.replace('\r\n','<br />')
  #try:
  db.posts.insert({'date':i,'title':title,'body':body})
  #except: 
  #  return render_template('uhoh.html')
  return render_template('index.html',blog_title=settings.blog_title)

@app.route('/edit/<post_id>',methods=['GET'])
def edit(post_id):
  post=db.posts.find_one({'_id':ObjectId(post_id)})
  return render_template('edit.html',blog_title=settings.blog_title,post=post)

@app.route('/edit/',methods=['POST'])
def pedit():
  title = request.form['title']
  body = request.form['body']#.replace('\r\n','<br />')
  #try:
  print(db.posts.update({'_id':ObjectId(request.form['post_id'])},{'date':i,'title':title,'body':body},safe=False,upsert=False))
  #except: 
  #  return render_template('uhoh.html')
  return render_template('index.html',blog_title=settings.blog_title)

@app.route('/remove/<post_id>',methods=['GET'])
def remove(post_id):
  title = db.posts.find_one({'_id':ObjectId(post_id)})
  print(db.posts.remove({'_id':ObjectId(post_id)}))
  return render_template('remove.html',blog_title=settings.blog_title,title=title)

if __name__ == "__main__":
  app.run(debug=True)

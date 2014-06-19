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
import datetime
import settings

app = Flask(__name__)
Bootstrap(app)

# Instanciate our variables for date and also for mongo here
date = datetime.datetime.now()
client = MongoClient()
db = client.coral



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
  body = request.form['body']
  #try:
  db.posts.insert({'date':"061814",'title':title,'body':body})
  #except: 
  #  return render_template('uhoh.html')
  return render_template('index.html',blog_title=settings.blog_title)


if __name__ == "__main__":
  app.run(debug=True)

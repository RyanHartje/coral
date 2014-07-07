'''
coral - a Python/Mongo blog using Flask, a web frameworks.
6-18-14
ryan@ryanhartje.com
http://github.com/ryanhartje/coral/

Please report any bugs at:
  https://github.com/RyanHartje/coral/issues/new
'''

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField,RadioField,SelectField,TextAreaField,SubmitField
from wtforms.validators import Required
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

app = Flask(__name__)
Bootstrap(app)

# Here is a debug error for more verbose output to the logging facility
#debug = False
debug = True

# Instanciate our variables for date and also for mongo here
app.config['SECRET_KEY'] = "#3d78jH}uys89sy"
date = datetime.datetime.now()
client = MongoClient()
db = client.coral
session = {'logged_in':False}
i = datetime.datetime.now()

# We can call this function elsewhere to return our (JSON) object
def getSettings():
  try:
    settings = db.settings.find_one({'name':'settings'})
  except:
    settings = {'title':'Coral','keywords':'','logo':'', 'perpage':25,'comments':'off','_id':ObjectId(1) }
  print("Finding settings")
  return settings

def getSidebar():
  try:
    sidebar = db.settings.find_one({'name':'sidebar'})
  except:
    sidebar = {'sidebar':'<h4>By:</h4><br><a href="http://austindevlabs.com" target="_NEW"> \
        <img src="http://austindevlabs.com/logo.png"></a>'}

  if debug:
    print("Sidebar: %s" % sidebar)
  return sidebar

class settingsForm(Form):
  class Meta:
    csrf = True
    csrf_secret = b'#3d78jH}uys89sy'

  title = StringField('Site Title:',validators=[Required()])
  comments = RadioField('Comments',choices=[('on','On'),('off','Off')],validators=[Required()])
  # perpage
  gcode = TextAreaField('Google Analytics Code:')
  keywords = StringField('Keywords:')
  submit = SubmitField('Submit')

@app.route('/')
def index():

  # Sort our posts decending from latest to eldest
  #     This does not raise an error if posts is blank so no catch is necessary
  posts = db.posts.find().sort('date',-1)

  # call the sidebar and settings so we can call our index
  sidebar = getSidebar() 
  settings = getSettings()
  return render_template('index.html',posts=posts,settings=settings,logged_in=session['logged_in'],sidebar=sidebar)

@app.route('/view/<postid>')
def view(postid):
  post = db.posts.find_one({'_id':ObjectId(postid)})
  if debug:
    print(post)

  settings = getSettings()
  sidebar = getSidebar()
  return render_template('view.html',settings=settings,post=post,logged_in=session['logged_in'],sidebar=sidebar)

@app.route('/add/',methods=['GET','POST'])
def add():
  settings = getSettings()
  sidebar = getSidebar()
  if request.method=='GET':
    return render_template('badd.html',settings=settings,logged_in=session['logged_in'])
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

    return redirect(url_for('index',settings=settings,sidebar=sidebar,logged_in=session['logged_in']))

@app.route('/edit/<post_id>',methods=['GET'])
def edit(post_id):
  settings = getSettings()
  post=db.posts.find_one({'_id':ObjectId(post_id)})
  return render_template('edit.html',settings=settings,post=post,logged_in=session['logged_in'])

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
  settings=getSettings()
  return redirect(url_for('index',settings=settings,posts=posts,logged_in=session['logged_in']))

@app.route('/remove/<post_id>',methods=['GET'])
def remove(post_id):
  title = db.posts.find_one({'_id':ObjectId(post_id)})
  print(db.posts.remove({'_id':ObjectId(post_id)}))
  return render_template('remove.html',settings=settings,title=title)

@app.route('/login/',methods=['GET','POST'])
def login():
  settings = getSettings()
  if request.method=='GET':
    return render_template('login.html',settings=settings,logged_in=session['logged_in'])

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

    return redirect(url_for('index',settings=settings,posts=posts,logged_in=session['logged_in']))

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
  settings = getSettings()
  form = settingsForm()

  # form.validate_on_submit is a boolean that is True 
  # on form submission, so no need to capture the POST method
  if form.validate_on_submit():
    flash("Settings Updated")
    title = form.title.data
    comments = form.comments.data
    gcode = form.gcode.data
    keywords = form.keywords.data

    # After, we clear the form data. 
    form.title.data=''
    form.comments.data=''
    form.gcode.data=''
    form.keywords.data=''

    user_input = { 'title': title, 'comments': comments, 'gcode': gcode, 'keywords': keywords, 'name':'settings'}

    if debug:
      print("Updating current settings: %s" % user_input)

    db.settings.update({'_id':ObjectId(settings['_id'])},user_input,upsert=False,safe=False)
    return redirect(url_for('settings',settings=settings,logged_in=session['logged_in'],form=form))
  elif not form.validate_on_submit() and request.method=='POST':
    flash("Error: Please choose a value for all settings")
  form.gcode.data = settings['gcode']
  return render_template('settings.html',settings=settings,logged_in=session['logged_in'],form=form)

@app.route('/settings/sidebar/', methods=['GET','POST'])
def sidebar():
  
  sidebar = getSidebar()
  settings = getSettings()
  if request.method=='GET':
    return render_template('sidebar.html',settings=settings,logged_in=session['logged_in'],sidebar=sidebar)

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
    return redirect(url_for('index',settings=settings,logged_in=session['logged_in'],posts=posts))
 

if __name__ == "__main__":
  app.run(host="0.0.0.0",debug=True)

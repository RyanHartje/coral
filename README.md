Coral
=========

Coral is a simple blog app written in Python.
Some of it's roadmap features include

  - Syntax Highlighting and Link detection
  - Authentication
  - Single Pageness

Version
----

.01

Dependencies
----

Install Python Libraries Flask, flask-bootstrap, and pymongo

```ssh
easy_install flask flask-bootstrap flask-moment pymongo wtforms
```

MongoDB

Mac OS X
```ssh
brew update
brew install mongodb
```
http://docs.mongodb.org/manual/tutorial/install-mongodb-on-os-x/

If you do not have Brew installed, first run:
```ssh
ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
```
Then start mongodb with brew's service feature:
```ssh
brew services start mongodb
```
You can also use this command with stop and restart inplace of start to stop and restart mongo if needed.

You should now be able to drop into the Mongo Shell with:
```ssh
mongo
```

Centos [Instructions coming soon]
```ssh
yum install mongodb
```

I would like to add support for other databases, so making this extensible should be roadmapped. 

Tech
-----------

Coral uses a number of open source projects to work properly:

* [Flask] - A Web Frameworks for Python
* [pymongo] - Mongo Bindings for Python
* [Twitter Bootstrap] - great UI boilerplate for modern web apps
* [jQuery] - a javascript library
* [CKEditor] - a RTF themer for textarea that runs in javascript

Installation
--------------

```ssh
git clone https://github.com/ryanhartje/coral.git
```

Usage
----

```ssh
python app/app.py
```

License
----

MIT

[Twitter Bootstrap]:http://twitter.github.com/bootstrap/
[jQuery]:http://jquery.com
[Flask]:http://flask.pocoo.org/
[pymongo]:http://api.mongodb.org/python/current/
[CKEditor]:http://docs.ckeditor.com/#!/guide

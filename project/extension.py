from flask_pymongo import PyMongo
from flask import  session, redirect, flash
from functools import wraps
import json
from bson import ObjectId

mongo = PyMongo()

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            if session['user']['permission']:
                return f(*args, **kwargs)
            else:
                session.clear()
                flash('You have to waited for permission to access')
                return redirect('/')
        else:
            flash('You have to logged in first')
            return redirect('/')
    return wrap
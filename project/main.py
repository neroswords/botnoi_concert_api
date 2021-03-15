from flask import Blueprint, render_template, url_for, request, session, redirect, flash, send_from_directory, current_app
from .extension import mongo, login_required
from project.models.user import User
from bson import ObjectId
main = Blueprint('main',__name__)


@main.route('/',methods=['GET'])
def landing():
    if 'logged_in' in session.keys() and session['logged_in']:
        return redirect('/concert/list')
    return render_template('landing.html')

@main.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        return User().signup()

@main.route('/signout',methods=['GET'])
def signout():
    return User().signout()


@main.route('/login',methods=['POST'])
def login():
    return User().login()

@main.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(current_app.config['DOWNLOAD_FOLDER']+'/image', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@main.route('/images/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['DOWNLOAD_FOLDER']+'/image', filename)

@main.route('/permission', methods=['GET','POST'])
def permission():
    user_collection = mongo.db.users
    if not session['user']['isAdmin']:
        return redirect('/')
    if request.method == 'GET':
        user_data = user_collection.find({'permission':False})
        return render_template('permission.html', userList=user_data)
    elif  request.method == 'POST':
        user_id = [ObjectId(x) for x in request.get_json()]
        user_collection.update_many({"_id":{"$in":user_id}},{"$set":{'permission':True}})
        return {"success": "success"},200
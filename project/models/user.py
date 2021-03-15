from flask import jsonify, request, Markup, flash, render_template, session, redirect
from passlib.hash import pbkdf2_sha256
from project.extension import mongo, JSONEncoder
import uuid
import json
class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        json_user = json.loads(JSONEncoder().encode(user))
        session['user'] = json_user
        return json_user,200

    def signup(self):
        print(request.form)
        user ={
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "permission":False,
            "isAdmin":False
        }

        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        user_collection = mongo.db.users
        if user_collection.find_one({"email": user['email']}):
            return jsonify({"error":"This email address already in use"})
        if user_collection.insert_one(user):
            return self.start_session(user)
            # return jsonify(user),200
        return jsonify({"error":"signup failed, please try again later."}),400

    def login(self):
        user_collection = mongo.db.users
        user_define = user_collection.find_one({"email":request.form.get('email')})
        if user_define:
            if pbkdf2_sha256.verify(request.form.get('password'),user_define['password']):
                return self.start_session(user_define)
            else:
                return jsonify({"error": "your password was wrong, please cheack again"})
        return jsonify({"error": "Invalid email please cheack your email again or signup"})
    
    def signout(self):
        session.clear()
        return redirect('/')
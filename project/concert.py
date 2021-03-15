from flask import Blueprint, render_template, url_for, request, session, redirect, flash, current_app
from .extension import mongo, login_required
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from bson import ObjectId
concert = Blueprint('concert',__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@concert.route('/list',methods=['GET'])
@login_required
def concert_list():
    concert_collection = mongo.db.concerts
    all_list = concert_collection.find({})
    concertList = list(all_list)
    return render_template('concert_list.html',concertList=concertList)

@concert.route('/create',methods=['POST'])
@login_required
def create_concert():
    if request.method == 'POST':
        concert_collection = mongo.db.concerts
        target = "/".join([current_app.config["UPLOAD_FOLDER"], 'concert'])
    
        if not os.path.isdir(target):
            os.mkdir(target)
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            extension = filename.split('.')[1]
            filename = request.form.get('title')+"&" + str(datetime.timestamp(datetime.now()))+'.'+extension
            file.save("/".join([target, filename]))
        data ={
                "title": request.form.get('title'),
                "link": request.form.get('link'),
                "price": float(request.form.get('price')),
                "payment": request.form.get('payment'),
                "date": request.form.get('date'),
                "info": request.form.get('info'),
                "image": filename,
                "status": "waited"
            }
        concert_collection.insert_one(data)
        return redirect('/concert/list')

@concert.route('/<id>/to_close',methods=['POST'])
@login_required
def closeConcert(id):
    concert_collection = mongo.db.concerts
    concert_collection.update_one({"_id":ObjectId(id)},{"$set":{'status':"close"}})
    return redirect("/concert/"+id)

@concert.route('/<id>/to_open',methods=['POST'])
@login_required
def openConcert(id):
    concert_collection = mongo.db.concerts
    concert_collection.update_one({"_id":ObjectId(id)},{"$set":{'status':"open"}})
    return redirect("/concert/"+id)

@concert.route('/closeorder',methods=['POST'])
@login_required
def closeorder():
    concert_collection = mongo.db.concerts
    concert_id = [ObjectId(x) for x in request.get_json()]
    concert_collection.update_many({"_id":{"$in":concert_id}},{"$set":{'status':"close"}})
    return {"success": "success"},200


@concert.route('/<id>',methods=['GET'])
@login_required
def info(id):
    concert_collection = mongo.db.concerts
    transaction_collection = mongo.db.transactions
    concert_define = concert_collection.find_one({'_id':ObjectId(id)})
    waited_trans = transaction_collection.find({"$and":[{"concert_id":ObjectId(id)},{"status":"waited"}]})
    purchased_trans = transaction_collection.find({"$and":[{"concert_id":ObjectId(id)},{"status":"purchased"}]})
    return render_template('concert_info.html',concert=concert_define, waited_transactions = waited_trans, purchased_transactions = purchased_trans)

@concert.route('/<id>/payment',methods=['POST'])
@login_required
def confirm(id):
    transaction_collection = mongo.db.transactions
    transaction_collection.update_one({"$and":[{'_id':ObjectId(request.get_json()['transid'])},{'concert_id':ObjectId(id)}]},{"$set":{"status":"purchased"}})
    return {},200

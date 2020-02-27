import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'fly_manager'
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_fly')
def get_fly():
    return render_template("fly.html", fly=mongo.db.fly.find())


@app.route('/add_fly')
def add_fly():
    return render_template('addfly.html', fly=mongo.db.fly.find())


@app.route('/insert_fly', methods=['POST'])
def insert_fly():
    fly = mongo.db.fly
    fly.insert_one(request.form.to_dict())
    return redirect(url_for('get_fly'))


@app.route('/edit_fly/<fly_id>')
def edit_fly(fly_id):
    the_fly = mongo.db.fly.find_one({'_id': ObjectId(fly_id)})
    all_species = mongo.db.species.find()
    return render_template('editfly.html', fly=the_fly, species=all_species)


@app.route('/update.fly/<fly_id>', methods=['POST'])
def update_fly(fly_id):
    fly = mongo.db.fly
    fly.update({'_id': ObjectId(fly_id)},
    {
        'name': request.form.get('name'),
        'hook': request.form.get('hook'),
        'thread': request.form.get('thread'),
        'rib': request.form.get('rib'),
        'head': request.form.get('head'),
        'body': request.form.get('body'),
        'thorax': request.form.get('thorax'),
        'legs': request.form.get('legs'),
        'hackle': request.form.get('hackle'),
        'species': request.form.get('species'),
        'link': request.form.get('link')
    })
    return redirect(url_for('get_fly'))


@app.route('/delete_fly/<fly_id>')
def delete_fly(fly_id):
    mongo.db.fly.remove({'_id': ObjectId(fly_id)})
    return redirect(url_for('get_fly'))


@app.route('/add_privacy')
def add_privacy():
    return render_template('privacy.html')


@app.route('/add_contact')
def add_contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')), debug=True)  # remember to change to false before final push to Heroku

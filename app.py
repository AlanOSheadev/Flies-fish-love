import os
from flask import Flask, render_template, redirect, request, url_for
from flask_paginate import Pagination, get_page_args
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'fly_manager'
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

# ----------- Home Page --------------

@app.route('/')
@app.route('/get_fly')
def get_fly():
    return render_template("fly.html", fly=mongo.db.fly.find().sort("name"))

# ----------- Add Fly Page --------------

@app.route('/add_fly')
def add_fly():
    return render_template('addfly.html', fly=mongo.db.fly.find())


@app.route('/insert_fly', methods=['POST'])
def insert_fly():
    fly = mongo.db.fly
    fly.insert_one(request.form.to_dict())
    return redirect(url_for('get_fly'))

# ----------- Edit Fly Page --------------

@app.route('/edit_fly/<fly_id>')
def edit_fly(fly_id):
    the_fly = mongo.db.fly.find_one({'_id': ObjectId(fly_id)})
    all_species = mongo.db.species.find()
    return render_template('editfly.html', fly=the_fly, species=all_species)


@app.route('/update.fly/<fly_id>', methods=['POST'])
def update_fly(fly_id):
    fly = mongo.db.fly
    fly.update({'_id': ObjectId(fly_id)}, {
        'name': request.form.get('name'),
        'species': request.form.get('species'),
        'hook': request.form.get('hook'),
        'thread': request.form.get('thread'),
        'rib': request.form.get('rib'),
        'head': request.form.get('head'),
        'body': request.form.get('body'),
        'thorax': request.form.get('thorax'),
        'legs': request.form.get('legs'),
        'wings': request.form.get('wings'),
        'tail': request.form.get('tail'),
        'hackle': request.form.get('hackle'),
        'link': request.form.get('link'),
        'submitted_by': request.form.get('submitted_by'),
        'delete': True
    })
    return redirect(url_for('get_fly'))


# ----------- Delete Fly Page --------------

@app.route('/delete_fly/<fly_id>')
def delete_fly(fly_id):
    mongo.db.fly.remove({'_id': ObjectId(fly_id)})
    return redirect(url_for('get_fly'))


# ----------- Privacy Page --------------

@app.route('/add_privacy')
def add_privacy():
    return render_template('privacy.html')


# ----------- Contact Page --------------

@app.route('/add_contact')
def add_contact():
    return render_template('contact.html')


# ----------- Search Fly by name Page --------------

@app.route('/search_flyname', methods=['GET', 'POST'])
def search_flyname():
    query = request.args.get('search')
    results = mongo.db.fly.find({'name': { "$regex": query, "$options": 'i' }}).sort('name')
    return render_template('searchflyname.html', results=results)


# def get_flys(offset=0, per_page=8):
#     fly = mongo.db.fly.find()
#     print("herl")
#     return fly[offset: offset + per_page]


# @app.route('/here')
# def showflys():
#     page, per_page, offset = get_page_args(page_parameter='page',
#                                            per_page_parameter='per_page')
#     total = mongo.db.fly.find().count()
#     paginatedflys = get_flys(offset=offset, per_page=per_page)
#     pagination = Pagination(page=page, per_page=per_page, total=total,
#                             css_framework='bootstrap4')
#     return render_template('searchflyname.html',
#                            flys=paginatedflys,
#                            page=page,
#                            per_page=per_page,
#                            pagination=pagination,
#                            )


# ----------- Search Fly by Submitted By Page --------------

@app.route('/search_flysubmited', methods=['GET', 'POST'])
def search_flysubmitted():
    query = request.args.get('searchsub')
    results = mongo.db.fly.find({'name': { "$regex": query, "$options": 'i' }}).sort('name')
    return render_template('searchflysubmitted.html', results=results)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')), debug=True)  # remember to change to false before final push to Heroku

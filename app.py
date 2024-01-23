#import sqlite3
import json
import requests
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import pymongo
from bson import json_util
import pprint
#from flask_cors import CORS, cross_origin

def parse_json(data):
    return json.loads(json_util.dumps(data))

def get_db_connection():
    #create mongodb client
    client = pymongo.MongoClient("localhost", 27017)
    #choose the db freegamefindings
    db = client.freegamefindings
    #then choose the table posts
    postsdb = db.posts
    return postsdb


app = Flask(__name__)

@app.route('/')
def index():
    postsdb = get_db_connection()
    posts = []
    for post in postsdb.find().limit(50):
        #find posts and add them to the array
        posts.append(post)
        #pprint.pprint(post)
    #return the array
    return render_template('index.html', posts=posts2)
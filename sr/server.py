#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, pandas, sqlite3, os
from flask import Flask, request, jsonify, json
from sqlite3 import Error
import query_pool
import crossdomain

app = Flask(__name__)

#Get currect directory
DIR_PATH = os.path.abspath(os.path.dirname(__file__))

DB_STORED_PATH = os.path.join(DIR_PATH, 'db')
DB_URI = os.path.join(DB_STORED_PATH, 'recommender.db')


@app.route("/api/user", methods=["POST"])
def add_user():
    user_id = request.json['user_id']

    return jsonify()


@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    return 


@app.route("/api/random/songs", methods=["GET"])
@crossdomain.cors(origin='*')
def get_random_songs():
    conn = query_pool.create_connection(DB_URI)

    songs = query_pool.get_random_songs(conn)

    json_string = songs.to_json(orient='records')
    response = jsonify(json.loads(json_string))
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(debug=True)


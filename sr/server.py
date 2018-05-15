#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, pandas, sqlite3, os
from flask import Flask, request, jsonify, json, session, flash, abort
from sqlite3 import Error
import query_pool
import crossdomain
import datetime

app = Flask(__name__)

#Get currect directory
DIR_PATH = os.path.abspath(os.path.dirname(__file__))

DB_STORED_PATH = os.path.join(DIR_PATH, 'db')
DB_URI = os.path.join(DB_STORED_PATH, 'recommender.db')


@app.route("/api/login", methods=["POST"])
@crossdomain.cors(origin='*')
def log_in():
    user_id = request.json['user_id']
    password = request.json['password']

    conn = query_pool.create_connection(DB_URI)
    login_return = query_pool.check_login(conn, user_id, password)

    if not login_return['success']:
        return jsonify({ 'status': -1 })
    
    user = login_return['user']
    
    session['logged_in'] = True
    session['user'] = user.to_dict(orient='records')[0]
    session['songs_recent'] = []

    return jsonify({ 'status': 1 })


@app.route("/api/logout")
@crossdomain.cors(origin='*')
def log_out():
    session['logged_in'] = False
    session['songs_recent'] = []
    return jsonify({ 'status': 1 })



@app.route("/api/song/listen", methods=["POST"])
@crossdomain.cors(origin='*')
def listen_song():
    if not session.get('logged_in'):
        return jsonify({'status': -1, 'errorMsg': 'You have not login!'})

    song_id = request.json['song_id']
    user_id = session.get('user')['user_id']
    current_time = datetime.datetime.now().replace(microsecond=0).isoformat()

    data_df = { 'user_id': [user_id], 'song_id': [song_id], 'timestamp': [current_time] }
    tracking_df = pandas.DataFrame(data_df)

    songs_recent = session.get('songs_recent')
    songs_recent.append(song_id)
    session['songs_recent'] = songs_recent

    conn = query_pool.create_connection(DB_URI)
    tracking_df.to_sql('trackings', conn, if_exists='append', index=False)
    song_df = query_pool.get_song(conn, song_id)

    song = song_df.to_dict(orient='records')[0]

    return jsonify({'song_info': song})



@app.route("/api/song/recommend", methods=["POST"])
@crossdomain.cors(origin='*')
def recommend_songs():
    if not session.get('logged_in'):
        return jsonify({ 'status': -1, 'errorMsg': 'You have not login!' })
    
    user_id = session.get('user')['user_id']
    songs_recent = session.get('songs_recent')

    conn = query_pool.create_connection(DB_URI)

    recommend_songs = query_pool.get_random_songs(conn)

    json_string = recommend_songs.to_json(orient='records')
    response = jsonify(json.loads(json_string))
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/api/whoimi")
@crossdomain.cors(origin='*')
def whoimi():
    user = session.get('user')

    return jsonify(user)

@app.route("/api/history")
@crossdomain.cors(origin='*')
def history():
    songs = session.get('songs_recent')

    return jsonify(songs)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)


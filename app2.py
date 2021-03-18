#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 22:06:51 2021

@author: yatin
"""
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from datetime import datetime

# Init app
app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Song Class/Model

class Song(db.Model):
    
    __tablename__ = 'song'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    duration = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    
    
    def __init__(self, name, duration, time):
        self.name=name
        self.duration=duration
        self.time=time
        
# Song Schema
class SongSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'duration', 'time')
        
# Init Schema
song_schema = SongSchema()
songs_schema = SongSchema(many=True)


# Podcast Class/Model
class Podcast(db.Model):
    
    __tablename__ = 'podcast'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    duration = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    host = db.Column(db.String(100))
    participant = db.Column(db.String(100))
    
    def __init__(self, name, duration, time, host, participant):
        self.name=name
        self.duration=duration
        self.time=time
        self.host=host
        self.participant=participant
        
# Podcast Schema
class PodcastSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'duration', 'time', 'host', 'participant')
        
# Init Schema
podcast_schema = PodcastSchema()
podcasts_schema = PodcastSchema(many=True)

# Audiobook Class/Model
class Audiobook(db.Model):
    
    __tablename__ = 'Audiobook'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    author = db.Column(db.String(100))
    narrator = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, title, author, narrator, duration, time):
        self.title=title
        self.author=author
        self.narrator=narrator
        self.duration=duration
        self.time=time
        
# Audiobook Schema
class AudiobookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author', 'narrator', 'duration', 'time')
        
# Init Schema
audiobook_schema = AudiobookSchema()
audiobooks_schema = AudiobookSchema(many=True)




# Create a AudioFile metadata

@app.route('/<audio_type>', methods=['POST'])
def add_product(audio_type):
    audio1="song"
    if audio_type == audio1:
        name = request.json['name']
        duration = request.json['duration']
        #time = request.json['time']
        time=datetime.now()
        new_song = Song(name, duration, datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"))
        db.session.add(new_song)
        db.session.commit()  
        return song_schema.jsonify(new_song)
    
    audio2="podcast"
    if audio_type == audio2:
        name = request.json['name']
        duration = request.json['duration']
        #time = request.json['time']
        time1=datetime.now()
        time=datetime.strptime(time1.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        host = request.json['host']
        participant = request.json['participant']
        new_podcast = Podcast(name, duration, time, host, participant)
        db.session.add(new_podcast)
        db.session.commit()  
        return podcast_schema.jsonify(new_podcast)
    
    audio3="audiobook"
    if audio_type == audio3:
        title = request.json['title']
        author = request.json['author']
        narrator = request.json['narrator']
        duration = request.json['duration']
        #time = request.json['time']
        time1=datetime.now()
        time=datetime.strptime(time1.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        
        new_audiobook = Audiobook(title, author, narrator, duration, time)
        db.session.add(new_audiobook)
        db.session.commit()  
        return audiobook_schema.jsonify(new_audiobook)

# Get all AudioFile metadata

@app.route('/<audio_type>', methods=['GET'])
def get_products(audio_type):
    if audio_type == "song":
        all_songs = Song.query.all()
        result =   songs_schema.dump(all_songs)
        return jsonify(result)    
    
    if audio_type == "podcast":
        all_podcasts = Podcast.query.all()
        result =   podcasts_schema.dump(all_podcasts)
        return jsonify(result)
    
    if audio_type == "audiobook":
        all_audiobooks = Audiobook.query.all()
        result =   audiobooks_schema.dump(all_audiobooks)
        return jsonify(result)    

# Get a AudioFile metadata

@app.route('/<audio_type>/<id>', methods=['GET'])
def get_product(audio_type, id):
    if audio_type == "song":
        song = Song.query.get(id)
        return song_schema.jsonify(song)

    if audio_type == "podcast":
        podcast = Podcast.query.get(id)
        return podcast_schema.jsonify(podcast) 
    
    if audio_type == "audiobook":
        audiobook = Audiobook.query.get(id)
        return audiobook_schema.jsonify(audiobook)

# Update a AudioFile metadata

@app.route('/<audio_type>/<id>', methods=['PUT'])
def Update_product(audio_type, id):
    if audio_type == "song":
        song = Song.query.get(id)
        name = request.json['name']
        duration = request.json['duration']
        #time = request.json['time']    
        song.name = name
        song.duration = duration
        time1=datetime.now()
        time=datetime.strptime(time1.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        song.time = time
        db.session.commit()
        return song_schema.jsonify(song)
    
    if audio_type == "podcast":
        podcast = Podcast.query.get(id)
        name = request.json['name']
        duration = request.json['duration']
        #time = request.json['time']    
        time1=datetime.now()
        time=datetime.strptime(time1.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        host=request.json['host']
        participant=request.json['participant']
        podcast.name = name
        podcast.duration = duration
        podcast.time = time
        podcast.host = host
        podcast.participant = participant
        db.session.commit()
        return podcast_schema.jsonify(podcast)
    
    if audio_type == "audiobook":
        audiobook = Audiobook.query.get(id)
        title = request.json['title']
        author=request.json['author']
        narrator=request.json['narrator']
        duration = request.json['duration']
        #time = request.json['time']    
        time1=datetime.now()
        time=datetime.strptime(time1.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        
        audiobook.title = title
        audiobook.author = author
        audiobook.narrator = narrator
        audiobook.duration = duration
        audiobook.time = time
        
        db.session.commit()
        return audiobook_schema.jsonify(audiobook)

# Delete a AudioFile metadata
@app.route('/<audio_type>/<id>', methods=['DELETE'])
def delete_product(audio_type, id):
    if audio_type == "song":
        song = Song.query.get(id)
        db.session.delete(song)
        db.session.commit()
        return song_schema.jsonify(song)
    
    if audio_type == "podcast":
        podcast = Podcast.query.get(id)
        db.session.delete(podcast)
        db.session.commit()
        return podcast_schema.jsonify(podcast)
    
    if audio_type == "audiobook":
        audiobook = Audiobook.query.get(id)
        db.session.delete(audiobook)
        db.session.commit()
        return audiobook_schema.jsonify(audiobook)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)

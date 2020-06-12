from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
from bs4 import BeautifulSoup
import os
from timetable import TimeTable, SubID
from time import sleep
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
import translators as ts
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
import random
import dictionary
from sqlalchemy import CheckConstraint
from sqlalchemy.exc import IntegrityError
import time
from time import strftime


app = Flask(__name__)

app.config['SECRET_KEY'] = 'anirudhalderson'

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['WHOOSH_BASE'] = 'search'

db = SQLAlchemy(app)

admin = Admin(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    note_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_no = db.Column(db.String(30), nullable=False, unique=False)
    note = db.Column(db.Text, nullable=False, unique=False)


class Tasks(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    assigned_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tasks = db.Column(db.Text, nullable=False, unique=False)
    assigned_by = db.Column(db.String(20), nullable=False, unique=False)


about = '''
Hi I Am A WhatsApp Bot 
Coded By Anirudh MP.
Currently My Developer
Is Still Busy Developing Me.
I Am Limited As I Am In Beta Stage.

I Will Be Reloaded And Will Be Back.
'''

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Tasks, db.session))


@app.route('/')
def home():
    return "<h1>Hola Amigo</h1>"


@app.route('/sms', methods=['POST'])
def sms():
    msg = request.form.get('Body').lower()
    res = MessagingResponse()

    if msg[0:5] == 'about':
        res.message(about)
        return res

    if msg[0:4] == 'note':
        number = request.form.get('From')
        text = msg.split('note ')[1]
        user = User(user_no=number, note=text)
        db.session.add(user)
        db.session.commit()
        res.message('*Done Your Note Has Been Added Successfully*')
        return str(res)

    if msg[0:9] == 'get_notes':
        number = request.form.get('From')
        note = User.query.filter_by(user_no=number).all()
        for item in note:
            messag = f'*Note ID = {str(item.id)}* \n```{item.note}```'
            res.message(messag)
        return str(res)

    if msg[0:8] == 'get_note':
        number = request.form.get('From')
        try:
            note_id = msg.split('get_note ')[1]
            note = User.query.filter_by(id=note_id).first()
            if note.user_no == number:
                messag = f'*Note ID = {str(note.id)}* \n```{note.note}```'
                res.message(messag)
            else:
                res.message('*You Are Not Authorised To View Others NOTES*')
        except Exception:
            error = '*Please Provide Note ID*'
            res.message(error)
        return str(res)

    if msg[0:8] == 'del_note':
        number = request.form.get('From')
        try:
            note_id = msg.split('del_note ')[1]
            note = User.query.filter_by(id=note_id).first()
            if note.user_no == number:
                db.session.delete(note)
                db.session.commit()
                res.message(f'*Note With Note ID = {str(note.id)} Deleted Successfully*')
            else:
                res.message('*You Are Not Authorised To Delete Others NOTES*')
        except Exception:
            error = '*Please Provide Note ID*'
            res.message(error)
        return str(res)

    if msg[0:9] == 'translate':
        trans_msg = msg.split('translate ')[1]
        translated = ts.google(trans_msg, 'auto', 'en')
        translated_msg = f'{trans_msg}\n\n*ENGLISH*\n\t```{str(translated)}```'
        res.message(str(translated_msg))
        return str(res)

    if msg[0:6] == 'define':
        key = msg.split('define ')[1]
        meaning = dictionary.definition(key)
        res.message(f'*{key.upper()} Meaning*')
        j=0
        for i in meaning:
            j=j+1
            res.message(f'*{j}* ```{i["definition"].capitalize()}```')
        return str(res)

    if msg == 'tasks':
        all_tasks = Tasks.query.all()
        for task in all_tasks:
            dat = task.assigned_date.strftime('%d-%m-%Y')
            res.message(f'*Task No:{task.id}*\n*Date: *```{dat}```\n*Task: *{task.tasks}\nAssigned by: {task.assigned_by}')
        return str(res)


if __name__ == "__main__":
    app.run(debug=True)

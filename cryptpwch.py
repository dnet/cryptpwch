#!/usr/bin/env python

from __future__ import with_statement, print_function
from flask import Flask, render_template, request
from contextlib import closing
from sqlalchemy import create_engine, Table, Column, String, MetaData
from sqlalchemy.sql import select, update
from os import path
from crypt import crypt
from base64 import b64encode
import json

app = Flask(__name__)
CONFIG_FILE = path.join(path.dirname(__file__), 'config.json')

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        msg = process_post()
    else:
        msg = None
    return render_template('form.html', msg=msg, fields=request.form)

def process_post():
    if request.form['pw1'] != request.form['pw2']:
        return 'New passwords must match'
    if not request.form['pw1']:
        return 'Please enter a new password'
    config = get_config()
    username = Column(config['fields']['username'], String)
    password = Column(config['fields']['password'], String)
    users = Table(config['table'], MetaData(), username, password)
    with create_engine(config['db_url']).connect() as db:
        user_filter = username == request.form['user']
        with closing(db.execute(select([password], user_filter))) as userinfo:
            if userinfo.rowcount != 1:
                return 'Invalid username'
            (old_hash,) = userinfo.fetchone()
            if crypt(request.form['pw'], old_hash) != old_hash:
                return 'Invalid password'
        with file('/dev/random') as random:
            chunk = random.read(6)
        salt = '$6${random}$'.format(random=b64encode(chunk, './'))
        db.execute(update(users, user_filter,
            {password: crypt(request.form['pw1'], salt)}))
    return 'Password changed successfully'

def get_config():
    with file(CONFIG_FILE, 'rb') as cfg:
        return json.load(cfg)

if __name__ == '__main__':
    app.run(debug=True)

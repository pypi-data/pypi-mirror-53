#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/26 11:15
# @File    : example.py
# @author  : dfkai
# @Software: PyCharm
import logging as logger

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_curd_db import FlaskCurdDb

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
FlaskCurdDb(app, db, logger)
from flask_curd_db.db import CRUDMixin


class User(db.Model, CRUDMixin):
    name = db.Column(db.String(50))


@app.route("/")
def index():
    d = dict(name="good")
    user = User.insert(**d)
    if user:
        return user.get_dict()
    else:
        return "hello,world!"


if __name__ == '__main__':
    # db.drop_all()
    db.create_all()
    app.run()

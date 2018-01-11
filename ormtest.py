#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import reqparse, Api, Resource

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)



app.config[
    'SQLALCHEMY_DATABASE_URI'] = \
    "mysql://root:xxxx@10.xxx.xxxx:xx/test?charset=utf8"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# 建立user表
class Usr(db.Model):
    __tablename__ = 'usr'
    id = db.Column(db.Integer, primary_key=True)
    usrname = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.relationship('Phone', backref='user', lazy='dynamic')

    def __init__(self, username, email):
        self.usrname = username
        self.email = email

class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    factory = db.Column(db.String(20))
    userId = db.Column(db.Integer, db.ForeignKey('usr.id'))
    attr = db.relationship(
         'Atttr', backref='phone', lazy='dynamic')

    def __init__(self, name, factory, userId):
        self.name = name
        self.factory = factory
        self.userId = userId


class Atttr(db.Model):
    id = db .Column(db.Integer, primary_key=True)
    color = db.Column(db.String(20))
    price = db.Column(db.String(20))
    macId = db.Column(db.Integer, db.ForeignKey('phone.id'))

    def __init__(self, color, price, macId):
        self.color = color
        self.price = price
        self.macId = macId

#db.create_all()
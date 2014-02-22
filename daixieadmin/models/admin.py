# -*- coding: utf-8 -*-

from hashlib import md5

from flask.ext.login import UserMixin

from daixie import db

class Admin(db.Model, UserMixin):

    __tablename__ = 'admin'

    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(45), unique=True, nullable=False)
    passwd = db.Column('passwd', db.String(45), nullable=False)
    username = db.Column('passwd', db.String(45))

    
    def __init__(self, email, passwd):
        self.email = email
        self.passwd = md5(passwd).hexdigest()


    def __repr__(self):
        return '<User %r>' % self.email

# -*- coding: utf-8 -*-

from hashlib import md5

from daixieadmin.models import enum

from flask.ext.login import UserMixin

from daixieadmin import db

class Admin(db.Model, UserMixin):

    __tablename__ = 'admin'

    ADMIN_TYPE = enum(CS=0, ADMIN=1)

    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(45), unique=True, nullable=False)
    passwd = db.Column('passwd', db.String(45), nullable=False)
    type = db.Column('type', db.Integer, nullable=False)

    
    def __init__(self, email, passwd):
        self.email = email
        self.passwd = md5(passwd).hexdigest()
        self.type = Admin.ADMIN_TYPE.CS

    def __repr__(self):
        return '<ADMIN %r %s>' % (self.email, self.type)

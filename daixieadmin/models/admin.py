# -*- coding: utf-8 -*-

from hashlib import md5

from daixieadmin.models import enum

from flask.ext.login import UserMixin

from daixieadmin import db

class Admin(db.Model, UserMixin):

    __tablename__ = 'admin'

    ADMIN_TYPE = enum(CS=0, ADMIN=1, SOLVER=2)

    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(45), unique=True, nullable=False)
    passwd = db.Column('passwd', db.String(45), nullable=False)
    type = db.Column('type', db.Integer, nullable=False)
    qq = db.Column('qq', db.String(45), nullable=False)

    
    def __init__(self, email, passwd, qq=None):
        self.email = email
        self.passwd = md5(passwd).hexdigest()
        self.type = Admin.ADMIN_TYPE.CS
        self.qq = qq

    @property
    def user_type(self):
        if self.type == Admin.ADMIN_TYPE.CS:
            return u'客服'
        if self.type == Admin.ADMIN_TYPE.SOLVER:
            return u'解题员'

    def __repr__(self):
        return '<ADMIN %r %s>' % (self.email, self.type)
    
    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False           

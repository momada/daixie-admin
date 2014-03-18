# -*- coding: utf-8 -*-

from hashlib import md5

from daixieadmin.models import enum

from flask.ext.login import UserMixin

from daixieadmin import db

class User(db.Model, UserMixin):

    __tablename__ = 'user'

    ACTIVATE = enum(NO=0, YES=1)
    SEX = enum(MALE=0, FEMALE=1)
    USER_TYPE = enum(USER=0, SOLVER=1)

    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(45), unique=True, nullable=False)
    passwd = db.Column('passwd', db.String(45), nullable=False)
    activate = db.Column('activate', db.BOOLEAN, nullable=False)
    type = db.Column('type', db.Integer, nullable=False)
    nickname = db.Column('nickname', db.String(45), nullable=False)
    sex = db.Column('sex', db.Integer, nullable=False)
    description = db.Column('description', db.String(1000), nullable=False)
    qq = db.Column('qq', db.String(45), nullable=False)
    account = db.Column('account', db.FLOAT, nullable=False)

    
    def __init__(self, email, passwd, type=USER_TYPE.USER, nickname='', qq=None):
        self.email = email
        self.passwd = md5(passwd).hexdigest()
        self.activate = User.ACTIVATE.NO
        self.type = type
        self.nickname = nickname
        self.sex = User.SEX.MALE
        self.description = ''
        self.qq = qq
        self.account = 0

    @property
    def user_type(self):
        if self.type == User.USER_TYPE.USER:
            return u'普通用户'
        elif self.type == User.USER_TYPE.SOLVER:
            return u'解题员'

    def __repr__(self):
        return '<User %r>' % self.email

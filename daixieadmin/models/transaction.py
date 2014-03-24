# -*- coding: utf-8 -*-

from datetime import datetime

from daixieadmin.models import enum

from flask.ext.login import UserMixin

from daixieadmin import db

class Transaction(db.Model, UserMixin):

    __tablename__ = 'transaction'

    TYPE = enum(RECHARGE=0, PAY=1, REFUND=2)

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False)
    create_time = db.Column('create_time', db.DateTime, nullable=False)
    type = db.Column('type', db.Integer, nullable=False)
    description = db.Column('description', db.String, nullable=False)
    amount = db.Column('amount', db.FLOAT, nullable=False)
    account = db.Column('account', db.FLOAT, nullable=False)

    
    def __init__(self, user_id, amount, account, type, description):
        self.user_id = user_id
        self.amount = amount
        self.account = account
        self.type = type
        self.description = description
        self.create_time = datetime.now()


    def __repr__(self):
        return '<Transaction %r %r %r>' % (self.user_id, self.transaction_type, self.create_time)

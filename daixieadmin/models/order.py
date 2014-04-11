# -*- coding: utf-8 -*-

from datetime import datetime

from daixieadmin.models import enum

from flask.ext.login import UserMixin

from daixieadmin import db

class Order(db.Model, UserMixin):

    __tablename__ = 'order'

    STATUS = enum(CREATED=0, PAID=1, SOLVEING=2, FINISHED=3)

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer)
    cs_id = db.Column('cs_id', db.Integer)
    solver_id = db.Column('solver_id', db.Integer)
    status = db.Column('status', db.Integer, default = 0)
    create_time = db.Column('create_time', db.DateTime)
    require_time = db.Column('require_time', db.DateTime)
    expect_time = db.Column('expect_time', db.DateTime)
    title = db.Column('title', db.String)
    description = db.Column('description', db.String)
    supp_info = db.Column('supp_info', db.String)
    log = db.Column('log', db.String)
    grade = db.Column('grade', db.Integer)
    expect_hour = db.Column('expect_hour', db.FLOAT, default=0)
    actual_hour = db.Column('actual_hour', db.FLOAT, default=0)
    extra_item = db.Column('extra_item', db.String)
    extra_money = db.Column('extra_money', db.String)
    expect_order_price = db.Column('expect_order_price', db.FLOAT, nullable=False, default=0)
    actual_order_price = db.Column('actual_order_price', db.FLOAT, nullable=False, default=0)


    
    def __init__(self, user_id, cs_id, solver_id, require_time, expect_time, title, expect_hour, \
             expect_order_price, grade, actual_order_price=None, description=None, \
             extra_item=None, extra_money=None, log=''):
        self.user_id = user_id
        self.cs_id = cs_id
        self.solver_id = solver_id
        self.status = Order.STATUS.CREATED
        self.create_time = datetime.now()
        self.require_time = require_time
        self.expect_time = expect_time
        self.title = title
        self.description = description
        self.log = log
        self.grade = grade
        self.expect_hour = expect_hour
        self.actual_hour = None
        self.extra_item = extra_item
        self.extra_money = extra_money
        self.expect_order_price = expect_order_price
        self.actual_order_price = actual_order_price

    @property
    def user_email(self):
        from daixieadmin.biz.user import UserBiz
        user = UserBiz.get_user_by_id(self.user_id)
        return user.email

    @property
    def cs_email(self):
        from daixieadmin.biz.admin import AdminBiz
        cs = AdminBiz.get_admin_by_id(self.cs_id)
        return cs.email

    @property
    def solver_email(self):
        from daixieadmin.biz.user import UserBiz
        solver = UserBiz.get_user_by_id(self.solver_id)
        return solver.email

    def __repr__(self):
        return '<Order %r %r %r %r>' % (self.id, self.user_id, self.cs_id, self.solver_id)

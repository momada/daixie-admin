# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, redirect, render_template, request, abort

from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired

from flask.ext.login import login_required, current_user

from daixieadmin.biz.order import OrderBiz
from daixieadmin.utils.error import DaixieError, fail, success
from daixieadmin.models.admin import Admin

mod = Blueprint('order', __name__)

@mod.route('/create_order')
@login_required
def create_order():
    '''
    创建订单
    '''
    form = OrderForm()
    if not form.validate_on_submit():
        return render_template('general/create.html', form=form)
    order = None
    form.populate_obj(order)
    try:
        ret = OrderBiz.create_order(order)
    except DaixieError as e:
        fail(e)
        return render_template('order/create.html', form=form)
    success(ret)
    return redirect(url_for('.my_list'))

@mod.route('/my_list')
@login_required
def my_list():
	'''
	查看我的所有订单
	'''
	order_list = OrderBiz.get_order_list_by_admin_id(current_user.id)
	return render_template('order/list.html', order_list=order_list)

@mod.route('/order_list/<int:page>')
@login_required
def order_list(page=1):
    '''
    查看所有订单
    '''
    pager = None
    pager = OrderBiz.get_order_list_by_pager(page)
    return render_template('order/list.html', order_list=pager, paginate=True)

@mod.route('/more_info/<int:id>')
@login_required
def more_info(id):
	order = OrderBiz.get_order_by_id(id)
	if current_user.type == Admin.ADMIN_TYPE.CS:
		return render_template('order/more_info_for_cs.html', order=order)
	else:
		return render_template('order/more_info_for_admin.html', order=order)

class OrderForm(Form):
    id = TextField(u'订单编号')
    user_id = TextField(u'用户编号')
    cs_id = TextField(u'客服编号')
    solver_id = TextField(u'解题员编号')
    status = TextField(u'订单状态')
    create_time = TextField(u'创建时间')
    require_time = TextField(u'要求时间')
    expect_time = TextField(u'预计时间')
    title = TextField(u'标题')
    description = TextField(u'描述')
    supp_info = TextField(u'辅助信息')
    log = TextField(u'日志')
    expect_hour = TextField(u'预计耗时')
    actual_hour = TextField(u'实际耗时')
    extra_item = TextField(u'其他事项')
    extra_money = TextField(u'其他金额')
    order_price = TextField(u'订单价格')
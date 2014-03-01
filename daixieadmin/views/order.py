# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, redirect, render_template, request, abort

from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired

from flask.ext.login import login_required, current_user

from daixieadmin.biz.order import OrderBiz
from daixieadmin.biz.user import UserBiz
from daixieadmin.biz.admin import AdminBiz

from daixieadmin.utils.error import DaixieError, fail, success
from daixieadmin.models.admin import Admin
from daixieadmin.models.order import Order

mod = Blueprint('order', __name__)

@mod.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    '''
    创建订单
    '''
    form = OrderForm()
    if not form.validate_on_submit():
        return render_template('order/create.html', form=form)
    user = UserBiz.get_user_by_email(form.user_id.data)
    cs = AdminBiz.get_admin_by_email(form.cs_id.data)
    solver = UserBiz.get_user_by_email(form.solver_id.data)
    order = Order(user.id, cs.id, solver.id, form.require_time.data, form.expect_time.data, 
        form.title.data, form.expect_hour.data, form.order_price.data, form.grade.data, 
        form.description.data, form.supp_info.data, form.extra_item.data, form.extra_money.data, 
        form.log.data)
    try:
        ret = OrderBiz.create_order(order)
    except DaixieError as e:
        fail(e)
        return render_template('order/create.html', form=form)
    success(ret)
    return redirect(url_for('.my_list'))

@mod.route('/my_list')
@mod.route('/my_list/<int:page>')
@login_required
def my_list(page=1):
	'''
	查看我的所有订单
	'''
	pager = OrderBiz.get_order_list_by_admin_id(current_user.id, page=1)
	return render_template('order/list.html', order_list=pager, paginate=True)

@mod.route('/order_list')
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

@mod.route('/edit_order/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    order = OrderBiz.get_order_by_id(id)
    form = OrderForm(obj=order)
    if not form.validate_on_submit():
        if current_user.type == Admin.ADMIN_TYPE.CS:
            return render_template('order/edit_order_for_cs.html', form=form, id=id)
        else:
            return render_template('order/edit_order_for_admin.html', form=form, id=id)
    form.populate_obj(order)
    #修改订单
    try:
        ret = OrderBiz.edit_order(order)
        success(ret)
    except DaixieError as e:
        fail(e)

    return redirect(url_for('admin.home'))

class OrderForm(Form):
    status_choices = [('0', u'已创建‘'), ('1', u'已付款'), ('2', u'解决中'), ('3', u'已完成')]

    id = TextField(u'订单编号')
    user_id = TextField(u'用户编号', validators=[DataRequired()])
    cs_id = TextField(u'客服编号')
    solver_id = TextField(u'解题员编号')
    status = SelectField(u'订单状态', choices=status_choices, default='0')
    create_time = TextField(u'创建时间')
    require_time = TextField(u'要求时间')
    expect_time = TextField(u'预计时间')
    title = TextField(u'标题')
    description = TextField(u'描述')
    supp_info = TextField(u'辅助信息')
    log = TextAreaField(u'日志')
    grade = TextField(u'订单级别')
    expect_hour = TextField(u'预计耗时')
    actual_hour = TextField(u'实际耗时')
    extra_item = TextField(u'其他事项')
    extra_money = TextField(u'其他金额')
    order_price = TextField(u'订单价格')
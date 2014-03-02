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
    user = UserBiz.get_user_by_email(form.user_email.data)
    cs = AdminBiz.get_admin_by_email(form.cs_email.data)
    solver = UserBiz.get_user_by_email(form.solver_email.data)
    order = Order(user.id, cs.id, solver.id, form.require_time.data, form.expect_time.data, 
        form.title.data, form.expect_hour.data, form.order_price.data, form.grade.data, 
        form.description.data, form.supp_info.data, form.extra_item.data, form.extra_money.data, 
        form.log.data)
    print "***************"
    print order
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
    if(current_user.type == Admin.ADMIN_TYPE.CS):
        return redirect(url_for('.edit_order_for_cs', id=id))
    else:
        return redirect(url_for('.edit_order_for_admin', id=id))


@mod.route('/edit_order_for_cs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_order_for_cs(id):
    order = OrderBiz.get_order_by_id(id)
    form = CSEditOrderForm(obj=order)
    form.log.data = ''
    if not form.validate_on_submit():
        return render_template('order/edit_order_for_cs.html', form=form, id=id, order=order)
    order.status = form.status.data
    order.expect_time = form.expect_time.data
    order.title = form.title.data
    order.description = form.description.data
    order.supp_info = form.supp_info.data
    order.log = order.log+form.log.data
    order.grade = form.grade.data
    order.expect_hour = form.expect_hour.data
    order.actual_hour = form.actual_hour.data if form.actual_hour.data == '' else None

    #修改订单
    try:
        ret = OrderBiz.edit_order(order)
        success(ret)
    except DaixieError as e:
        fail(e)

    return redirect(url_for('admin.home'))

@mod.route('/edit_order_for_admin/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_order_for_admin(id):
    order = OrderBiz.get_order_by_id(id)
    form = AdminEditOrderForm(obj=order)
    if not form.validate_on_submit():
        return render_template('order/edit_order_for_admin.html', form=form, id=id, order=order)
    
    cs = AdminBiz.get_admin_by_email(form.cs_email.data)
    solver = UserBiz.get_user_by_email(form.solver_email.data)

    order.cs_id = cs.id
    order.solver_id = solver.id
    order.status = form.status.data
    order.require_time = form.require_time.data
    order.expect_time = form.expect_time.data
    order.title = form.title.data
    order.description = form.description.data
    order.supp_info = form.supp_info.data
    order.log = form.log.data
    order.grade = form.grade.data
    order.expect_hour = form.expect_hour.data
    order.actual_hour = form.actual_hour.data
    order.extra_item = form.extra_item.data
    order.extra_money = form.extra_money.data

    #修改订单
    try:
        ret = OrderBiz.edit_order(order)
        success(ret)
    except DaixieError as e:
        fail(e)

    return redirect(url_for('admin.home'))

class OrderForm(Form):
    status_choices = [('0', u'已创建‘'), ('1', u'已付款'), ('2', u'解决中'), ('3', u'已完成')]

    user_email = TextField(u'用户邮箱', validators=[DataRequired()])
    cs_email = TextField(u'客服邮箱', validators=[DataRequired()])
    solver_email = TextField(u'解题员邮箱', validators=[DataRequired()])
    status = SelectField(u'订单状态', choices=status_choices, default='0')
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

class CSEditOrderForm(Form):
    status_choices = [('0', u'已创建‘'), ('1', u'已付款'), ('2', u'解决中'), ('3', u'已完成')]

    status = SelectField(u'订单状态', choices=status_choices, default='0')
    expect_time = TextField(u'预计时间')
    title = TextField(u'标题')
    description = TextField(u'描述')
    supp_info = TextField(u'辅助信息')
    log = TextAreaField(u'新日志')
    grade = TextField(u'订单级别')
    expect_hour = TextField(u'预计耗时')
    actual_hour = TextField(u'实际耗时')

class AdminEditOrderForm(Form):
    status_choices = [('0', u'已创建‘'), ('1', u'已付款'), ('2', u'解决中'), ('3', u'已完成')]

    cs_email = TextField(u'客服邮箱')
    solver_email = TextField(u'解题员邮箱')
    status = SelectField(u'订单状态', choices=status_choices, default='0')
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
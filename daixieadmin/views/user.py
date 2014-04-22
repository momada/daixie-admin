# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, redirect, render_template, request, abort

from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired

from flask.ext.sqlalchemy import Pagination
from flask.ext.login import login_required, current_user

from daixieadmin.biz.user import UserBiz
from daixieadmin.biz.admin import AdminBiz
from daixieadmin.models.user import User
from daixieadmin.models.admin import Admin
from daixieadmin.utils.error import DaixieError, fail, success, j_ok, j_err
from daixieadmin.utils.http import get_arg

mod = Blueprint('user', __name__)

@mod.route('/home')
@login_required
def home():
	'''
	主页
	'''
	return render_template('user/home.html')

@mod.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	'''
	个人信息
	'''
	form = ProfileForm(obj=current_user)
	if not form.validate_on_submit():
		return render_template('user/setting.html', form=form)
	user = current_user
	form.populate_obj(user)
	#修改个人信息
	try:
		ret = UserBiz.edit_user_profile(user)
		success(ret)
	except DaixieError as e:
		fail(e)
	return redirect(url_for('.profile'))

@mod.route('/users', methods=['GET'])
@login_required
def j_search_user():
	email = request.args.get('email', '')
	query = request.args.get('query', '')
	page = get_arg('page', 1)
	type = request.args.get('type', '')
	#print "query is ",query

	if(type == 'user'):
		type = User.USER_TYPE.USER

	try:
		if email:
			user = UserBiz.get_user_by_email(email, type)
			users_pager = Pagination(None, 1, 1, 1, [user])
		else:
			users_pager = UserBiz.get_by_like(query, type, page, per_page=10)
	except DaixieError as e:
		return j_err(e)

	users = [{
	'id': user.email,
	'text': user.email,
	'account': user.account
	} for user in users_pager.items if user]

	return j_ok(u'搜索成功', items=users, pages=users_pager.pages)

@mod.route('/solvers', methods=['GET'])
@login_required
def j_search_solvers():
	email = request.args.get('email', '')
	query = request.args.get('query', '')
	page = get_arg('page', 1)
	type = request.args.get('type', '')

	type = Admin.ADMIN_TYPE.SOLVER

	try:
		if email:
			user = AdminBiz.get_cs_by_email(email, type)
			users_pager = Pagination(None, 1, 1, 1, [user])
		else:
			users_pager = AdminBiz.get_by_like(query, type, page, per_page=10)
	except DaixieError as e:
		return j_err(e)

	users = [{
	'id': user.email,
	'text': user.email
	} for user in users_pager.items if user]

	return j_ok(u'搜索成功', items=users, pages=users_pager.pages)
class ProfileForm(Form):
	sex_choices = [('0', u'男'), ('1', u'女')]
	email = TextField(u'登录邮箱', validators=[DataRequired(), Email()])
	nickname = TextField(u'昵称',[Regexp('[\s|\S]')])
	sex = SelectField(u'性别', choices=sex_choices, default='0')
	description = TextAreaField(u'自我介绍',[Regexp('[\s|\S]')])
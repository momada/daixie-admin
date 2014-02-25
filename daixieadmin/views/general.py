# -*- coding: utf-8 -*-


from flask import Blueprint, url_for, redirect, render_template
from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Email, Regexp, DataRequired, EqualTo
                            
from flask.ext.login import login_required, current_user

from daixieadmin.utils.error import DaixieError, fail, success

from daixieadmin.models.admin import Admin
from daixieadmin.biz.admin import AdminBiz

mod = Blueprint('general', __name__)

@mod.route('/', methods=['GET', 'POST'])
def index():
    '''
    网站首页
    '''
    if current_user.is_authenticated():
        return redirect(url_for('.add_cs')) ###
    return redirect(url_for('.login'))

@mod.route('/add_cs', methods=['GET', 'POST'])
@login_required
def add_cs():
    '''
    add cs
    '''
    form = RegisterForm()
    if not form.validate_on_submit():
        print form.errors
        return render_template('general/add_cs.html', form=form, hide_login_link=True)
    cs = Admin(form.email.data, form.passwd.data)

    try:
        ret = AdminBiz.add_CS(cs)
    except DaixieError as e:
        fail(e)
        return render_template('general/add_cs.html', form=form, hide_login_link=True)        
    success(ret)
    return redirect(url_for('.add_cs'))

@mod.route('/login', methods=['GET','POST'])
def login():
    '''
    登录
    '''
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template('general/login.html', form=form)
    email = form.email.data
    passwd = form.passwd.data
    auto = form.auto.data

    admin = Admin(email, passwd)
    try:
        ret = AdminBiz.admin_login(admin, auto)
    except DaixieError as e:
        fail(e)
        return render_template('general/login.html', form=form)
    success(ret)
    return redirect(url_for('.add_cs'))

@mod.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    '''
    注销
    '''
    try:
        AdminBiz.admin_logout()
    except DaixieError as e:
        fail(e)
    return redirect(url_for('.index'))

@mod.route('/daixie_rule')
@login_required
def daixie_rule():
    return render_template("general/daixie_rule.html")

class LoginForm(Form):
    email = TextField(u'邮箱', validators=[DataRequired(), Email()])
    passwd = PasswordField(u'密码', validators=[DataRequired(),Regexp('[\w\d-]{5,20}')])
    auto = BooleanField(u'自动登录', default=False)
class RegisterForm(Form):
    email = TextField(u'邮箱地址*', validators=[DataRequired(), Email()])
    passwd = PasswordField(u'密码*', validators=[DataRequired(),Regexp('[\w\d-]{5,20}', message=u'5-20位')])
    passwd_confirm = PasswordField(u'确认密码*', validators=[DataRequired(), EqualTo('passwd', message=u'密码不一致')])
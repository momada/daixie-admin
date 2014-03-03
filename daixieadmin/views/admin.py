# -*- coding: utf-8 -*-


from flask import Blueprint,  url_for, redirect, render_template
from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectField
from wtforms.validators import Email, Regexp, DataRequired, EqualTo
                            
from flask.ext.login import login_required, current_user

from daixieadmin.utils.error import DaixieError, fail, success

from daixieadmin.models.admin import Admin
from daixieadmin.models.user import User

from daixieadmin.biz.admin import AdminBiz
from daixieadmin.biz.user import UserBiz


mod = Blueprint('admin', __name__)

@mod.route('/home')
@login_required
def home():
	'''
	主页
	'''
	return render_template('admin/home.html')

@mod.route('/cs_list', methods=['GET', 'POST'])
@login_required
def cs_list():
    '''
    网站首页
    '''
    if current_user.type == Admin.ADMIN_TYPE.ADMIN:
        all_cs = AdminBiz.get_all_CS();
        all_user = UserBiz.get_all_user();
        return render_template('admin/cs_list.html', cs_list=all_cs, user_list=all_user)
    else:
        return render_template('general/index.html')

@mod.route('/add_cs', methods=['GET', 'POST'])
@login_required
def add_cs():
    '''
    创建解题员和客服
    '''
    if current_user.type == Admin.ADMIN_TYPE.ADMIN:
        form = RegisterForm()
        if not form.validate_on_submit():
            print form.errors
            return render_template('admin/add_cs.html', form=form)
        try:
            if form.user_type.data=='0':
                cs = Admin(form.email.data, form.passwd.data)
                ret = AdminBiz.add_CS(cs)
            else:
                solver = User(form.email.data, form.passwd.data, form.user_type.data)
                ret = UserBiz.add_solver(solver)
            success(ret)
        except DaixieError as e:
            fail(e)
            return redirect(url_for('.add_cs'))
        return redirect(url_for('.add_cs'))     
    else:
        return render_template('general/index.html')

@mod.route('/update_cs/<int:id>', methods=['GET', 'POST'])
@login_required
def update_cs(id):
    '''
    update cs
    '''
    cs=AdminBiz.get_admin_by_id(id);
    form = AccountForm();
    if not form.validate_on_submit():
        return render_template('admin/update.html',form=form,id=id,type="CS")
    try:
        cs.passwd = form.passwd.data
        ret = AdminBiz.cs_commit_update(cs=cs)
    except DaixieError as e:
        fail(e)
        return redirect(url_for('.cs_list'))     
    success(ret)
    return redirect(url_for('.cs_list')) 

@mod.route('/update_solver/<int:id>', methods=['GET', 'POST'])
@login_required
def update_solver(id):
    '''
    update solver
    '''
    solver=UserBiz.get_user_by_id(id);
    form = AccountForm();
    if not form.validate_on_submit():
        return render_template('admin/update.html',form=form,id=id,type="SOLVER")
    try:
        solver.passwd = form.passwd.data
        ret = UserBiz.solver_commit_update(solver=solver)
    except DaixieError as e:
        fail(e)
        return redirect(url_for('.cs_list'))     
    success(ret)
    return redirect(url_for('.cs_list')) 

@mod.route('/delete_cs', methods=['GET', 'POST'])
@mod.route('/delete_cs/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_cs(id):
    '''
    delete cs
    '''
    cs = AdminBiz.get_admin_by_id(id)
    try:
        ret = AdminBiz.delete_CS(cs=cs)
    except DaixieError as e:
        fail(e) 
    success(ret)
    return redirect(url_for('.cs_list'))

@mod.route('/delete_solver', methods=['GET', 'POST'])
@mod.route('/delete_solver/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_solver(id):
    '''
    delete cs
    '''
    solver = UserBiz.get_user_by_id(id)
    try:
        ret = UserBiz.delete_solver(solver)
        success(ret)
    except DaixieError as e:
        fail(e) 
    
    return redirect(url_for('.cs_list'))

class RegisterForm(Form):
    user_type_choices = [('0', u'客服'), ('1', u'解题员')]

    user_type=SelectField(u'用户类型', choices=user_type_choices, default='0')
    email = TextField(u'邮箱地址*', validators=[DataRequired(), Email(message=u'请填写正确的邮箱地址')])
    passwd = PasswordField(u'密码*', validators=[DataRequired(),Regexp('[\w\d-]{6,20}', message=u'密码必须为6-20位')])
    passwd_confirm = PasswordField(u'确认密码*', validators=[DataRequired(), EqualTo('passwd', message=u'密码不一致')])

class AccountForm(Form):
    passwd = PasswordField(u'新密码*', validators=[DataRequired(),Regexp('[\w\d-]{6,20}', message=u'密码必须为6-20位')])
    passwd_confirm = PasswordField(u'确认密码*', validators=[DataRequired(), EqualTo('passwd', message=u'密码不一致')])

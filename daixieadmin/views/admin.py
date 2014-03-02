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

@mod.route('/management', methods=['GET', 'POST'])
def management():
    '''
    网站首页
    '''
    if current_user.is_authenticated() and current_user.type==1:
        form = RegisterForm()
        all_cs = AdminBiz.get_all_CS();
        all_solver = UserBiz.get_all_solver();
        if not form.validate_on_submit():
            print form.errors
            return render_template('admin/cs_list.html', cs_list=all_cs, solver_list=all_solver ,form=form)
        if form.user_type.data=='0':
            cs = Admin(form.email.data, form.passwd.data)
            try:
                ret = AdminBiz.add_CS(cs)
            except DaixieError as e:
                fail(e)
                return redirect(url_for('.management'))     
            success(ret)
        else:
            solver = User(form.email.data, form.passwd.data)
            try:
                ret = UserBiz.add_solver(solver)
            except DaixieError as e:
                fail(e)
                return redirect(url_for('.management'))     
            success(ret)
        return redirect(url_for('.management'))
    elif current_user.is_authenticated() :
        return render_template('general/index.html')
    return redirect(url_for('.login'))
    
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
        return redirect(url_for('.management'))     
    success(ret)
    return redirect(url_for('.management')) 

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
        return redirect(url_for('.management'))     
    success(ret)
    return redirect(url_for('.management')) 

@mod.route('/add_cs', methods=['GET', 'POST'])
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
    return redirect(url_for('.management'))

@mod.route('/add_css', methods=['GET', 'POST'])
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
    
    return redirect(url_for('.management'))

class RegisterForm(Form):
    user_choices = [('0', u'客服'), ('1', u'解题员')]
    user_type=SelectField(u'性别', choices=user_choices, default='0')
    email = TextField(u'邮箱地址*', validators=[DataRequired(), Email()])
    passwd = PasswordField(u'密码*', validators=[DataRequired(),Regexp('[\w\d-]{5,20}', message=u'5-20位')])
    passwd_confirm = PasswordField(u'确认密码*', validators=[DataRequired(), EqualTo('passwd', message=u'密码不一致')])

class AccountForm(Form):
    passwd = PasswordField(u'密码*', validators=[DataRequired(),Regexp('[\w\d-]{5,20}', message=u'5-20位')])
    passwd_confirm = PasswordField(u'确认密码*', validators=[DataRequired(), EqualTo('passwd', message=u'密码不一致')])

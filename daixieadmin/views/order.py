# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, redirect, render_template, request,send_from_directory,make_response

from flask_wtf import Form

from werkzeug.utils import secure_filename

from wtforms import TextField, FloatField, SelectField, DateTimeField, TextAreaField, DateTimeField,IntegerField
from wtforms.validators import DataRequired,  Length, Regexp, Email, NumberRange, Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired

from flask.ext.login import login_required, current_user

from daixieadmin.biz.order import OrderBiz
from daixieadmin.biz.user import UserBiz
from daixieadmin.biz.admin import AdminBiz

from daixieadmin.utils.error import DaixieError, fail, success
from daixieadmin.utils.tools import save_file_with_order_id
from daixieadmin.utils.form import User_Exist
from daixieadmin.models.admin import Admin
from daixieadmin.models.order import Order
from daixieadmin import app
from daixieadmin.views import j_login_required

mod = Blueprint('order', __name__)

@mod.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    '''
    创建订单
    '''
    if not current_user.is_authenticated():
        return redirect(url_for('general.index'))    
    form = OrderForm()
    if not form.validate_on_submit():
        return render_template('order/create.html', form=form, nav_order_manage='active')

    
    file = request.files['supp_info'] 
    if file :   
        if not allowed_file(file.filename):
            fail("file type error")
            return render_template('order/create.html', form=form, nav_order_manage='active')

    user = UserBiz.get_user_by_email(form.user_email.data)

    cs = AdminBiz.get_admin_by_email(form.cs_email.data)
    solverid = 0
    if form.solver_email.data:
        solver = AdminBiz.get_solver_by_email(form.solver_email.data)
        solverid = solver.id


    order = Order(user.id, cs.id, solverid, form.require_time.data, form.expect_time.data, 
        form.title.data, form.expect_hour.data, form.expect_order_price.data, 
        0, form.grade.data, form.description.data, form.extra_item.data, form.extra_money.data, form.log.data)

    
    try:
        ret = OrderBiz.create_order(order)
    except DaixieError as e:
        fail(e)
        return render_template('order/create.html', form=form, nav_order_manage='active')   

    if file :
        order_id = order.id
        save_file_with_order_id(order_id, file)
        order.supp_info = secure_filename(file.filename)
    
    try:
        OrderBiz.edit_order(order)
    except DaixieError as e:
        fail(e)
        return render_template('order/create.html', form=form, nav_order_manage='active')

    success(ret)
    return redirect(url_for('.my_list'))

@mod.route('/download/<int:id>', methods=['POST', 'GET'])
@j_login_required
def download_file(id):
    order = OrderBiz.get_order_by_id(id).first()
    filename = order.supp_info
    path = app.config['DIR_RESOURCES'] +'/'+ str(id) +'/'
    print "file to be downloaded is at : ", path
    return send_from_directory(path, filename, as_attachment=True)

def allowed_file(filename):
    return True
    #return '.' in filename and \
     #      filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@mod.route('/my_list')
@login_required
def my_list(page=1):
    '''
    查看我的所有订单
    '''
    
    if not current_user.is_authenticated():
        return redirect(url_for('general.index'))    
    searchform = SearchForm()
    pager = None
    if current_user.type == Admin.ADMIN_TYPE.CS or current_user.type == Admin.ADMIN_TYPE.ADMIN:
        pager = OrderBiz.get_order_list_by_admin_id(current_user.id, page=1)
    if current_user.type == Admin.ADMIN_TYPE.SOLVER:
        pager = OrderBiz.get_order_list_by_solver_id(current_user.id, page=1)
    return render_template('order/list.html',searchform = searchform, my_list =pager, type=1, nav_order_manage='active')

@mod.route('/search_order',methods=['POST'])
@login_required
def search_order():
    if not current_user.is_authenticated():
        return redirect(url_for('general.index'))
    searchform = SearchForm()
    print "order : ",searchform.order_id.data, "solver :", searchform.solver_id.data
    result = OrderBiz.search_order_by_pager(1,searchform.order_id.data,searchform.solver_id.data,searchform.require_time.data)
    return render_template('order/list.html', searchform = searchform, order_list=result, type=type, nav_order_manage='active')

@mod.route('/order_list')
@login_required
def order_list(page=1):
    '''
    查看所有订单
    '''

    if not current_user.is_authenticated():
        return redirect(url_for('general.index'))    
    searchform = SearchForm()

    pager = None
    pager = OrderBiz.get_order_list_by_pager(page)
    return render_template('order/list.html', searchform = searchform, order_list=pager, type=0, nav_order_manage='active')

@mod.route('/due_order')
@mod.route('/due_order/<int:page>')
@login_required
def due_order(page=0):
    '''
    
    '''

    if not current_user.is_authenticated():
        return redirect(url_for('general.index'))    
    searchform = SearchForm()
    if page == 0:
        pager = None
        pager = OrderBiz.get_due_order_by_pager(1)
        return render_template('order/list.html', searchform = searchform, order_list=pager, type=2, nav_order_manage='active')
    else :
        pager = None
        pager = OrderBiz.get_due_order_by_pager(page)
        return render_template('order/morelist.html', searchform = searchform, order_list=pager, type=2, nav_order_manage='active')

@mod.route('/order_list/<int:page>')
@login_required
def order_list_page(page=1):
    '''
    查看所有订单
    '''
    if not current_user.is_authenticated():
        raise u'权限不足'    
    pager = None
    pager = OrderBiz.get_order_list_by_pager(page)
    return render_template('order/morelist.html', order_list=pager, paginate=True, nav_order_manage='active')

@mod.route('/my_list/<int:page>')
@login_required
def my_list_page(page=1):
    '''
    查看所有订单
    '''
    if not current_user.is_authenticated():
        raise u'权限不足'    
    pager = None
    if current_user.type == Admin.ADMIN_TYPE.CS:
        pager = OrderBiz.get_order_list_by_admin_id(current_user.id, page)
    if current_user.type == Admin.ADMIN_TYPE.SOLVER:
        pager = OrderBiz.get_order_list_by_solver_id(current_user.id, page)
    return render_template('order/morelist.html', my_list =pager, paginate=True, nav_order_manage='active', tpye=1)    


@mod.route('/more_info/<int:id>')
@login_required
def more_info(id):
    if not current_user.is_authenticated():
        fail(u'权限不足')
        return redirect(url_for('general.index'))
  
    order = OrderBiz.get_order_by_id(id).first()
    if current_user.type == Admin.ADMIN_TYPE.CS:
		return render_template('order/more_info_for_cs.html', order=order, nav_order_manage='active')
    if current_user.type == Admin.ADMIN_TYPE.ADMIN:
        return render_template('order/more_info_for_admin.html', order=order, nav_order_manage='active')
    if current_user.type == Admin.ADMIN_TYPE.SOLVER:
        return render_template('order/more_info_for_solver.html', order=order, nav_order_manage='active')

@mod.route('/edit_order/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    if not current_user.is_authenticated():
        return redirect(url_for('general.index'))
    if(current_user.type == Admin.ADMIN_TYPE.SOLVER):
        fail(u'用户权限不足')
        return redirect(url_for('general.index'))    
    if(current_user.type == Admin.ADMIN_TYPE.CS):
        return redirect(url_for('.edit_order_for_cs', id=id))
    else:
        return redirect(url_for('.edit_order_for_admin', id=id))


@mod.route('/edit_order_for_cs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_order_for_cs(id):
    if not current_user.is_authenticated():
        return redirect(url_for('general.index'))
    if current_user.type != Admin.ADMIN_TYPE.CS:
        fail(u"用户权限不足")
        return redirect(url_for('general.index'))

    order = OrderBiz.get_order_by_id(id).first()
    form = CSEditOrderForm(obj=order)
    form.log.data = ''
    if not form.validate_on_submit():
        print "show order editing"
        return render_template('order/edit_order_for_cs.html', form=form, id=   id, order=order, nav_order_manage='active')
    
    file = request.files['supp_info']    
    if order.status <= form.status.data:
        order.status = form.status.data
    order.expect_time = form.expect_time.data
    order.title = form.title.data
    order.description = form.description.data
    order.log = order.log+form.log.data
    order.grade = form.grade.data
    order.expect_hour = form.expect_hour.data
    order.actual_hour = form.actual_hour.data

    if order.status == '3' and form.actual_order_price.data != 0 and form.actual_order_price is not None:
        order.actual_order_price = form.actual_order_price.data

    if file:
        save_file_with_order_id(id, file)
        print file.name
        order.supp_info = secure_filename(file.filename)

    #修改订单
    try:
        ret = OrderBiz.edit_order(order)
        success(ret)
    except DaixieError as e:
        fail(e)
        return render_template('order/edit_order_for_cs.html', form=form, id=id, order=order, nav_order_manage='active')

    return redirect(url_for('admin.home'))

@mod.route('/edit_order_for_admin/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_order_for_admin(id):
    if not current_user.is_authenticated() :
        return redirect(url_for('general.index'))    
    if current_user.type != Admin.ADMIN_TYPE.ADMIN:
        fail(u"用户权限不足")
        return redirect(url_for('general.index'))

    order = OrderBiz.get_order_by_id(id).first()
    form = AdminEditOrderForm(obj=order)
    if not form.validate_on_submit():
        return render_template('order/edit_order_for_admin.html', form=form, id=id, order=order, nav_order_manage='active')
    
    file = request.files['supp_info']    
    
    cs = AdminBiz.get_admin_by_email(form.cs_email.data)
    solver = AdminBiz.get_solver_by_email(form.solver_email.data)

    order.cs_id = cs.id
    order.solver_id = solver.id
    if order.status <= form.status.data:
        order.status = form.status.data
    order.require_time = form.require_time.data
    order.expect_time = form.expect_time.data
    order.title = form.title.data
    order.description = form.description.data
    order.log = form.log.data
    order.grade = form.grade.data
    order.expect_hour = form.expect_hour.data
    order.actual_hour = form.actual_hour.data
    order.extra_item = form.extra_item.data
    if order.status == '3' and form.actual_order_price.data != 0 and form.actual_order_price.data is not None:
        order.actual_order_price = form.actual_order_price.data

    if file:
        save_file_with_order_id(id, file)
        order.supp_info = secure_filename(file.filename)

    #修改订单
    try:
        ret = OrderBiz.edit_order(order)
        success(ret)
    except DaixieError as e:
        fail(e)
        return render_template('order/edit_order_for_admin.html', form=form, id=id, order=order, nav_order_manage='active')

    return redirect(url_for('admin.home'))

class OrderForm(Form):
    status_choices = [('0', u'已创建'), ('2', u'正在解决'), ('3', u'已解决')]
    grade_choices = [('0', u'产品A'), ('1', u'产品B'), ('2', u'产品C'), ('3', u'产品D'),('4', u'产品E')]

    user_email = TextField(u'用户邮箱', validators=[DataRequired(), Email(message=u'请填写正确的邮箱地址'), User_Exist()])
    cs_email = TextField(u'客服邮箱', validators=[DataRequired(), Email(message=u'请填写正确的邮箱地址')])
    solver_email = TextField(u'解题员邮箱')
    status = SelectField(u'订单状态', choices=status_choices, default='0')
    require_time = DateTimeField(u'要求完成时间', validators=[DataRequired()])
    expect_time = DateTimeField(u'预计完成时间', validators=[DataRequired()])
    title = TextField(u'标题', validators=[DataRequired()])
    description = TextAreaField(u'描述')
    supp_info= FileField(u'辅助信息')
    log = TextAreaField(u'日志')
    grade = SelectField(u'订单级别', choices=grade_choices, default='0')
    expect_hour = FloatField(u'预计耗时')
    actual_hour = FloatField(u'实际耗时')
    extra_item = TextField(u'其他事项')
    extra_money = FloatField(u'其他金额')
    expect_order_price = FloatField(u'预计订单价格')
    actual_order_price = FloatField(u'实际订单价格')

class CSEditOrderForm(Form):
    status_choices = [('0', u'已创建'), ('2', u'正在解决'), ('3', u'已解决')]
    grade_choices = [('0', u'产品A'), ('1', u'产品B'), ('2', u'产品C'), ('3', u'产品D')]

    solver_email = TextField(u'解题员邮箱', validators=[Email(message=u'请填写正确的邮箱地址')])
    status = SelectField(u'订单状态', choices=status_choices, default='0')
    expect_time = DateTimeField(u'预计完成时间', validators=[DataRequired()])
    title = TextField(u'标题')
    description = TextField(u'描述')
    supp_info= FileField(u'辅助信息')
    log = TextAreaField(u'新日志')
    grade = SelectField(u'订单级别', choices=grade_choices, default='0')
    expect_hour = FloatField(u'预计耗时')
    actual_hour = FloatField(u'实际耗时')
    actual_order_price = FloatField(u'实际订单价格', validators=[NumberRange(0)])

class AdminEditOrderForm(Form):
    status_choices = [('0', u'已创建'), ('2', u'正在解决'), ('3', u'已解决')]
    grade_choices = [('0', u'产品A'), ('1', u'产品B'), ('2', u'产品C'), ('3', u'产品D')] 


    cs_email = TextField(u'客服邮箱', validators=[DataRequired(), Email(message=u'请填写正确的邮箱地址')])
    solver_email = TextField(u'解题员邮箱', validators=[DataRequired(), Email(message=u'请填写正确的邮箱地址')])
    status = SelectField(u'订单状态', choices=status_choices, default='0')
    require_time = DateTimeField(u'要求完成时间', validators=[DataRequired()])
    expect_time = DateTimeField(u'预计完成时间', validators=[DataRequired()])
    title = TextField(u'标题')
    description = TextField(u'描述')
    supp_info= FileField(u'辅助信息')
    log = TextAreaField(u'日志')
    grade = SelectField(u'订单级别', choices=grade_choices, default='0')
    expect_hour = FloatField(u'预计耗时',validators=[DataRequired()])
    actual_hour = FloatField(u'实际耗时')
    extra_item = TextField(u'其他事项')
    actual_order_price = FloatField(u'实际订单价格', validators=[NumberRange(0)])

class SearchForm(Form):

    require_time = DateTimeField(u'要求完成时间')
    solver_id = IntegerField(u' 解题员编号',default='')
    order_id = IntegerField(u'订单编号',default='')
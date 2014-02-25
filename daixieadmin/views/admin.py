# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

from flask.ext.login import login_required

mod = Blueprint('admin', __name__)

@mod.route('/home')
@login_required
def home():
	'''
	主页
	'''
	return render_template('admin/home.html')


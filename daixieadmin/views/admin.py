# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, redirect, render_template, request, abort

from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired

from flask.ext.login import login_required, current_user

from daixie.utils.error import DaixieError, fail, success

mod = Blueprint('admin', __name__)

@mod.route('/home')
@login_required
def home():
	'''
	主页
	'''
	return render_template('admin/home.html')
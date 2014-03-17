# -*- coding: utf-8 -*-

from wtforms import ValidationError

from daixieadmin.utils.captcha import check_captcha

from daixieadmin.biz.user import UserBiz

#
# validators
#
class Captcha(object):
    '''
    验证码
    '''
    def __init__(self, message=u'验证码错误'):
        self.message = message

    def __call__(self, form, field):
        if not check_captcha(field.data):
            raise ValidationError(self.message)

class User_Exist(object):
	'''
	检验用户是否存在
	'''
	def __init__(self, message=u'用户不存在'):
		self.message = message

	def __call__(self, form, field):
		user = UserBiz.get_user_by_email(field.data)
		if not user:
			raise ValidationError(self.message)

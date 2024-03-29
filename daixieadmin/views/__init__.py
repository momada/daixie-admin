# -*- coding: utf-8 -*-

from functools import wraps

from flask.ext.login import current_user

from daixieadmin import login_manager
from daixieadmin.utils.error import j_err

def j_login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated():
            return j_err(u'您还没有登录')
        return func(*args, **kwargs)

    return wrapper


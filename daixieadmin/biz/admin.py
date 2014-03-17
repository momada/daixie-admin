# -*- coding: utf-8 -*-
from hashlib import md5

from flask.ext.login import login_user, logout_user

from daixieadmin.data.db import db_session
from daixieadmin.models.admin import Admin

from daixieadmin.utils.error_type import USER_DUPLICATE, USER_LOGOUT_OK, \
    USER_NOT_EXIST, USER_LOGIN_OK, USER_LOGOUT_FAIL, CS_DELETE_OK, CS_ADD_OK, CS_UPDATE_OK
from daixieadmin.utils.error import DaixieError

class AdminBiz:
    @staticmethod
    def get_admin_by_id(id):
        admin = db_session.query(Admin).get(id)
        return admin

    @staticmethod
    def get_admin_by_email(email):
        cs = db_session.query(Admin).filter_by(email=email).first()
        return cs

    @staticmethod
    def cs_commit_update(cs):
        try:
            cs.passwd = md5(cs.passwd).hexdigest()
            db_session.merge(cs)
            db_session.commit()
        except:
            db_session.rollback()
            raise
        return CS_UPDATE_OK

    @staticmethod
    def admin_login(admin, remember):
        u = db_session.query(Admin).filter_by(email=admin.email, passwd=admin.passwd).first()
        if not u:
            raise DaixieError(USER_NOT_EXIST)
        admin.id = u.id
        login_user(u, remember=remember)

        return USER_LOGIN_OK

    @staticmethod
    def admin_logout():
        try:
            logout_user()
        except:
            raise DaixieError(USER_LOGOUT_FAIL)
        return USER_LOGOUT_OK

    @staticmethod
    def add_CS(cs):
        if AdminBiz.get_admin_by_email(cs.email):
            raise DaixieError(USER_DUPLICATE)
        db_session.add(cs)
        db_session.commit()
        return CS_ADD_OK

    @staticmethod
    def delete_CS(cs):
        db_session.delete(cs)
        db_session.commit()
        return CS_DELETE_OK

    @staticmethod
    def get_all_CS():
        all_cs = db_session.query(Admin).filter(Admin.type == 'CS').all()   #pass the admin
        return all_cs

    @staticmethod
    def get_by_like(query, page=1, per_page=5):
        return Admin.query.filter(Admin.email.contains(query)).filter_by(type=Admin.ADMIN_TYPE.CS).paginate(page, per_page)

# -*- coding: utf-8 -*-

from flask.ext.login import login_user, logout_user

from daixieadmin.data.db import db_session
from daixieadmin.models.cust_supporter import Cust_Supporter
from daixieadmin.models.admin import Admin

from daixieadmin.utils.error_type import USER_DUPLICATE, USER_REGISTER_OK, USER_LOGOUT_OK, \
    USER_ACTIVATE_OK, USER_NOT_EXIST, USER_LOGIN_OK, USER_LOGOUT_FAIL, EDIT_USER_PROFILE_OK, \
    EDIT_USER_PROFILE_FAIL
from daixieadmin.utils.error import DaixieError

class AdminBiz:
    @staticmethod
    def get_admin_by_id(id):
        admin = db_session.query(admin).get(id)
        return admin

    # @staticmethod
    # def get_CS_by_email(email):
    #     cs = db_session.query(Cust_Supporter).filter_by(email=email).first()
    #     return cs

    # @staticmethod
    # def register(cs):
    #     if UserBiz.get_user_by_email(cs.email):
    #         raise DaixieError(USER_DUPLICATE)

    #     db_session.add(cs)
    #     db_session.commit()
        
    #     return USER_REGISTER_OK

    @staticmethod
    def admin_login(admin, remember):
        u = db_session.query(admin).filter_by(email=admin.email, passwd=admin.passwd).first()
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
    def add_CS():
        if Cust_SupporterBiz.get_user_by_email(cs.email):
            raise DaixieError(USER_DUPLICATE)

        db_session.add(cs)
        db_session.commit()

        return USER_REGISTER_OK

    # @staticmethod
    # def activate_user(cs):
    #     cs.activate = cs.ACTIVATE.YES
    #     db_session.commit()

    #     login_user(cs, remember=True)

    #     return USER_ACTIVATE_OK

    # @staticmethod
    # def edit_cs_profile(cs):
    #     try:
    #         db_session.add(cs)
    #         db_session.commit()
    #         login_user(cs, remember=True)
    #     except:
    #         raise DaixieError(EDIT_USER_PROFILE_FAIL)
    #     return EDIT_USER_PROFILE_OK
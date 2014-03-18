# -*- coding: utf-8 -*-
from hashlib import md5

from flask.ext.login import login_user, logout_user

from daixieadmin.data.db import db_session
from daixieadmin.models.user import User

from daixieadmin.utils.error_type import USER_DUPLICATE, USER_REGISTER_OK, USER_LOGOUT_OK, \
    USER_ACTIVATE_OK, USER_NOT_EXIST, USER_LOGIN_OK, USER_LOGOUT_FAIL, EDIT_USER_PROFILE_OK, \
    EDIT_USER_PROFILE_FAIL,SOLVER_DELETE_OK,SOLVER_UPDATE_OK, SOLVER_ADD_OK
from daixieadmin.utils.error import DaixieError

class UserBiz:
    @staticmethod
    def get_user_by_id(id):
        user = db_session.query(User).get(id)
        return user

    @staticmethod
    def get_all_user():
        all_solver = db_session.query(User).all()   #pass the admin
        return all_solver

    @staticmethod
    def get_user_by_email(email, type=None):
        if not type:
            user = db_session.query(User).filter_by(email=email).first()
        else:
            user = db_session.query(User).filter_by(email=email, type=type).first()
        return user

    @staticmethod
    def solver_commit_update(solver):
        try:
            solver.passwd = md5(solver.passwd).hexdigest()
            db_session.merge(solver)
            db_session.commit()
        except:
            db_session.rollback()
            raise
        return SOLVER_UPDATE_OK

    @staticmethod
    def register(user):
        if UserBiz.get_user_by_email(user.email):
            raise DaixieError(USER_DUPLICATE)
        db_session.add(user)
        db_session.commit()
        
        return USER_REGISTER_OK
    @staticmethod
    def add_solver(user):
        if UserBiz.get_user_by_email(user.email):
            raise DaixieError(USER_DUPLICATE)
        db_session.add(user)
        db_session.commit()
        return SOLVER_ADD_OK

    @staticmethod
    def delete_solver(user):
        db_session.delete(user)
        db_session.commit()
        return SOLVER_DELETE_OK

    @staticmethod
    def user_login(user, remember):
        u = db_session.query(User).filter_by(email=user.email, passwd=user.passwd).first()
        if not u:
            raise DaixieError(USER_NOT_EXIST)
        user.id = u.id
        login_user(u, remember=remember)

        return USER_LOGIN_OK

    @staticmethod
    def user_logout():
        try:
            logout_user()
        except:
            raise DaixieError(USER_LOGOUT_FAIL)
        return USER_LOGOUT_OK

    @staticmethod
    def activate_user(user):
        user.activate = User.ACTIVATE.YES
        db_session.commit()

        login_user(user, remember=True)

        return USER_ACTIVATE_OK

    @staticmethod
    def edit_user_profile(user):
        try:
            db_session.add(user)
            db_session.commit()
            login_user(user, remember=True)
        except:
            raise DaixieError(EDIT_USER_PROFILE_FAIL)
        return EDIT_USER_PROFILE_OK

    @staticmethod
    def get_by_like(query, type, page=1, per_page=5):
        return User.query.filter(User.email.contains(query)).filter_by(type=type).paginate(page, per_page)
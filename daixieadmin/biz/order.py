# -*- coding: utf-8 -*-

from daixieadmin.models.order import Order
from daixieadmin.data.db import db_session
from daixieadmin.utils.error import DaixieError
from daixieadmin.biz.user import UserBiz

from daixieadmin.utils.error_type import CREATE_ORDER_FAIL, CREATE_ORDER_OK, \
ORDER_NOT_EXIST, EDIT_ORDER_OK, EDIT_ORDER_FAIL

class OrderBiz:

	@staticmethod
	def get_order_by_id(id):
		return Order.query.filter_by(id=id).first()

	@staticmethod
	def get_order_list_by_user_id(user_id):
		return Order.query.filter_by(user_id=user_id).all();

	@staticmethod
	def get_order_list_by_solver_id(solver_id):
		return Order.query.filter_by(solver_id=solver_id).all();

	@staticmethod
	def get_order_list_by_admin_id(cs_id, page=1, per_page=30):
		return Order.query.filter_by(cs_id=cs_id).order_by(Order.id.desc()).paginate(page, per_page);

	@staticmethod
	def get_order_list_by_pager(page=1, per_page=30):
		return Order.query.order_by(Order.id.desc()).paginate(page, per_page);

	@staticmethod
	def create_order(order):
		try:
			db_session.add(order)
			db_session.commit()
		except:
			raise DaixieError(CREATE_ORDER_FAIL)
		return CREATE_ORDER_OK

	@staticmethod
	def edit_order(order):
		o = OrderBiz.get_order_by_id(order.id)
		if not o:
			raise DaixieError(ORDER_NOT_EXIST)

		if o.actual_order_price is not None and order.actual_order_price:
			try:
				amount = float(o.expect_order_price)-float(order.actual_order_price)
				UserBiz.recharge(o.user_id, amount*100)
			except DaixieError as e:
				raise e

		try:
			db_session.add(order)
			db_session.commit()
		except:
			raise DaixieError(EDIT_ORDER_FAIL)
		return EDIT_ORDER_OK
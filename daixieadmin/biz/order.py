# -*- coding: utf-8 -*-

from daixieadmin.models.order import Order

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
	def get_order_list_by_admin_id(id):
		return Order.query.filter_by(id=id).all();

	@staticmethod
	def get_order_list_by_pager(page=1, per_page=30):
		return Order.query.order_by(Order.id.desc()).paginate(page, per_page);
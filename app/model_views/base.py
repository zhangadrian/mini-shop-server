# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2020/3/3.
"""
from flask_admin.contrib.sqla import ModelView as _ModelView
from sqlalchemy import func
import json

__author__ = 'Allen7D'


class ModelView(_ModelView):
	column_exclude_list = ['create_time', 'update_time', 'delete_time', 'status']  # 隐藏字段
	page_size = 10  # 分页
	column_display_pk = True # 是否显示主键
	can_create = True  # 可新增, 默认True
	can_edit = True  # 可修改, 默认True
	can_delete = True  # 可删除, 默认True

	def __add__(self, other):
		self.column_exclude_list = list(set(self.column_exclude_list + other.column_exclude_list))

		return self

	def __getitem__(self, item):
		attr = getattr(self, item)
		# 将字符串转为JSON
		if isinstance(attr, str):
			try:
				attr = json.loads(attr)
			except ValueError:
				pass
		return attr

	def set_attrs(self, **kwargs):
		# 快速赋值，用法: set_attrs(form.data)
		for key, value in kwargs.items():
			if hasattr(self, key) and key != 'id':
				setattr(self, key, value)

	def keys(self):
		# 在 app/app.py中的 JSONEncoder中的 dict(o)使用
		# 在此处，整合要输出的属性：self.fields
		return self.fields

	def hide(self, *keys):
		for key in keys:
			# 使用exclude，在 Model层和 Service层等任意的操作中，已经隐藏的属性无法再添加
			# self.exclude.append(key)
			if key in self.fields:
				self.fields.remove(key)
		return self

	def append(self, *keys):
		for key in keys:
			if key not in self.fields:
				self.fields.append(key)
		return self

	# 对于查询，进行条件过滤
	def get_query(self):
		return self.session.query(self.model).filter(self.model.status == 1)

	# 对于查询统计，进行条件过滤
	def get_count_query(self):
		return self.session.query(func.count('*')).filter(self.model.status == 1)

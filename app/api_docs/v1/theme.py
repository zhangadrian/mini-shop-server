# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2018/12/4.
"""
from app.libs.swagger_filed import inject, IntegerPathFiled, ArrayQueryField

__author__ = 'Allen7D'


theme_id = IntegerPathFiled(name='id', description="theme id", enum=[1, 2, 3, 4, 5, 100], default=1, required=True)
theme_ids = ArrayQueryField(name='ids', description='theme id 多选', item_type='integer', enum=[1, 2, 3, 4, 5], default=1,
                      required=True)
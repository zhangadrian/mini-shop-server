# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2018/11/26.
"""
from app.libs.swagger_filed import BodyField

__author__ = 'Allen7D'

name = BodyField('name', 'string', '店铺名称', ['Tit'])
mobile = BodyField('mobile', 'string', '手机号', ['13758787058'])
poi_id = BodyField('poi_id', 'string', '店铺ID', ['1234567890'])
address = BodyField('address', 'string', '店铺地址', ['广州'])
latitude = BodyField('latitude', 'integer', '维度', [1234567890])
longitude = BodyField('longitude', 'integer', '经度', [1234567890])

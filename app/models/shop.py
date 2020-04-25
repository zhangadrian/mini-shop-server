# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2018/7/6.
"""
from sqlalchemy import Column, Integer, SmallInteger, String, Float, Text

from app.models.base import Base

__author__ = "Allen7D"


class Shop(Base):
    __tablename__ = "shop"
    id = Column(Integer, primary_key=True, autoincrement=True)
    poi_id = Column(String(250), unique=True, comment="店铺ID")
    name = Column(String(250), unique=True, comment="店铺ID")
    address = Column(String(250), comment="店铺地址")
    mobile = Column(String(255), comment="店铺电话")
    latitude = Column(Integer, comment="维度")
    longitude = Column(Integer, comment="经度")
    fields = ["poi_id", "name", "address", "mobile", "latitude", "longitude"]

    def keys(self):
        self.hide('id')
        return self.fields

# _*_ coding: utf-8 _*_

from sqlalchemy import Column, Integer, SmallInteger, String, Float, Text

from app.models.base import Base

__author__ = "adhcczhang"


class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True, autoincrement=True)
    poi_id = Column(String(250), unique=True, comment="店铺ID")
    user_openid = Column(String(50), unique=True, comment='用户openid')
    shop_owner_openid = Column(String(50), unique=True, comment='店铺openid')
    user_nickname = Column(String(24), comment='用户昵称')
    shop_owner_nickname = Column(String(24), comment='店铺昵称')
    group_name = Column(String(250), comment='群名称')
    fields = ["poi_id", "user_openid", "shop_owner_openid", "user_nickname", "shop_owner_nickname", 'group_name']

    def keys(self):
        self.hide('id')
        return self.fields

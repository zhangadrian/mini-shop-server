# _*_ coding: utf-8 _*_

from sqlalchemy import Column, Integer, SmallInteger, String, Float, Text
from sqlalchemy import and_
from app.models.base import Base

__author__ = "adhcczhang"


class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True, autoincrement=True)
    poi_id = Column(String(100), comment="店铺ID")
    user_openid = Column(String(50), comment='用户openid')
    shop_owner_openid = Column(String(50), comment='店铺openid')
    user_nickname = Column(String(24), comment='用户昵称')
    shop_owner_nickname = Column(String(24), comment='店铺昵称')
    group_name = Column(String(100), comment='群名称')
    group_id = Column(String(100), default='', comment='企业微信的群聊ID')
    fields = ["poi_id", "user_openid", "shop_owner_openid", "user_nickname", "shop_owner_nickname", 'group_name']

    def keys(self):
        self.hide('id')
        return self.fields

    @staticmethod
    def shop_group_count(poi_id, open_id):
        shop_group_list = Group.query.filter(Group.poi_id == poi_id).all()
        user_group_list = Group.query.filter(Group.user_openid == open_id).all()
        res = {
            "shop_group_count": len(shop_group_list),
            "user_group_count": len(user_group_list),
            "shop_group_info": shop_group_list,
            "user_group_info": user_group_list,
        }
        return res

    @classmethod
    def get_shop_list(cls, user_id, shop_id_list):
        group_data_list = Group.query.filter(and_(Group.user_openid == user_id, Group.status == 2)).all()
        group_data_dict = {}
        for group_data in group_data_list:
            group_data_dict[group_data.poi_id] = 1

        res_dict = {}
        for shop_id in shop_id_list:
            if shop_id in group_data_dict:
                res_dict[shop_id] = 1
        return res_dict




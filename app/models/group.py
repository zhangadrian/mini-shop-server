# _*_ coding: utf-8 _*_

from sqlalchemy import Column, Integer, SmallInteger, String, Float, Text
from sqlalchemy import and_
from app.models.base import Base
from app.models.new_shop import NewShop as Shop

from time import time

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
        shop_data = Shop.query.filter(Shop.poi_id == poi_id).first()
        if shop_data:
            if not shop_data.status or int(shop_data.status) == 4:
                shop_group_list = Group.query.filter(and_(Group.poi_id == poi_id, Group.status == 3)).all()
                user_group_list = Group.query.filter(and_(Group.user_openid == open_id, Group.status == 2)).all()
                res = {
                    "invite_number": len(shop_group_list),
                    "shop_group_info": [],
                    "user_group_count": len(user_group_list),
                    "user_group_info": user_group_list,
                }
            else:
                shop_group_list = Group.query.filter(and_(Group.poi_id == poi_id, Group.status == 2)).all()
                user_group_list = Group.query.filter(and_(Group.user_openid == open_id, Group.status == 2)).all()
                res = {
                    "shop_group_count": len(shop_group_list),
                    "user_group_count": len(user_group_list),
                    "shop_group_info": shop_group_list,
                    "user_group_info": user_group_list,
                }
        else:
            user_group_list = Group.query.filter(and_(Group.user_openid == open_id, Group.status == 2)).all()
            res = {
                "shop_group_info": [],
                "user_group_count": len(user_group_list),
                "user_group_info": user_group_list,
            }
        return res

    @classmethod
    def get_new_group(cls, time_gap, poi_id):
        shop_group_list = Group.query.filter(and_(Group.poi_id == poi_id, Group.status == 2)).all()
        current_time = int(time())

        new_group_list = []
        for shop_group in shop_group_list:
            if current_time - shop_group.create_time < time_gap:
                new_group_list.append(shop_group)
        res = {
            "new_group_number": len(new_group_list),
            "new_group_info": new_group_list
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




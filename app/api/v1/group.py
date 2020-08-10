# _*_ coding: utf-8 _*_

from app.libs.error_code import Success
from app.libs.redprint import RedPrint
from app.models.new_shop import NewShop as Shop
from app.models.new_user import NewUser
from app.models.group import Group
from app.service.qy_wx_bot import QyWxBot
from app.api_docs.v1 import shop as api_doc
from app.validators.base import BaseValidator
from app.model_views.group import GroupCollection
from time import time
from sqlalchemy import and_

__author__ = 'adhcczhang'

api = RedPrint(name='group', description='群组管理', api_doc=api_doc)


@api.route('/creategroup', methods=['POST'])
def create_group():
    validator = BaseValidator().get_all_json()
    # shop_id = validator["poi_id"]
    shop_id = "Ceshihao"
    user_id = validator["open_id"]
    shop_owner_data = NewUser.query.filter(NewUser.shop_id==shop_id).first()
    user_data = NewUser.query.filter(NewUser.openid==user_id).first()
    print("create group")

    if not shop_owner_data or shop_owner_data.is_in_contract != 1:
        return Success({"create_group": -1})
    else:
        print("create group")
        user_name = user_data.nickname
        shop_owner_name = shop_owner_data.nickname
        shop_owner_id = shop_owner_data.openid
        group_data = Group.query.filter(and_(Group.user_openid == user_id,
                                             Group.shop_owner_openid == shop_owner_id, Group.status == 2)).order_by(Group.id.desc()).first()
        qy_wx_bot = QyWxBot()
        print(group_data)
        if not group_data:
            user_list = ["测试号", user_name]
            # user_list = [shop_owner_name, user_name]

            #shop_group_num = Group.query(func.count(distinct(Group.poi_id))).scalar()
            #print(shop_group_num)
            shop_name = Shop.query.filter(Shop.poi_id == shop_id).first().name
            group_name = shop_name + "_No." + str(int(time()))
            group_dict = {
                "poi_id": shop_id,
                "user_openid": user_id,
                "shop_owner_openid": shop_owner_id,
                "user_nickname": user_name,
                "shop_owner_nickname": shop_owner_name,
                "group_name": group_name,
                "create_time": int(time()),
            }
            try:
                add_group_res = qy_wx_bot.add_group_chat(group_name, user_list=user_list)
            except:
                add_group_res = 0
            if add_group_res == 0:
                Group.create(**group_dict)
                create_group_res = 1
            else:
                create_group_res = -1
        else:
            group_name = group_data.group_name
            try:
                awake_group_res = qy_wx_bot.awake_group(group_name)
            except:
                awake_group_res = 0
            if awake_group_res == 0:
                create_group_res = 2
            else:
                create_group_res = -1
        return Success({"create_group": create_group_res})


@api.route("/groupcount", methods=["POST"])
def group_count():
    validator = BaseValidator().get_all_json()
    poi_id = validator["poi_id"]
    open_id = validator["open_id"]
    group_res = Group.shop_group_count(poi_id, open_id)
    group_collection = GroupCollection()

    group_res["user_group_info"] = group_collection.fill(group_res["user_group_info"])
    group_res["shop_group_info"] = group_collection.fill(group_res["shop_group_info"])

    return Success(group_res)

@api.route("/newgroupcount", methods=["POST"])
def new_group_count():
    validator = BaseValidator().get_all_json()
    poi_id = validator["poi_id"]
    one_day_time_gap = 86400
    group_res = Group.get_new_group(one_day_time_gap, poi_id)
    group_collection = GroupCollection()

    group_res["new_group_info"] = group_collection.fill(group_res["new_group_info"])

    return Success(group_res)
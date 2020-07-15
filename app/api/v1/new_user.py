# _*_ coding: utf-8 _*_

from flask import g, session

from app.libs.enums import ScopeEnum
from app.libs.error_code import Success
from app.libs.redprint import RedPrint

from app.libs.token_auth import auth
from app.models.new_user import NewUser
from app.models.new_shop import NewShop as Shop
from app.models.group import Group
from app.model_views.shop import ShopCollection 
from app.api_docs.v1 import user as api_doc  # api_doc可以引入
from app.validators.base import BaseValidator
from app.validators.forms import ChangePasswordValidator
from app.service.wx_token import WxToken
from app.service.callback import Callback
from sqlalchemy import and_
import time

__author__ = 'adhcczhang'

# 直接将api文档的内容放入RedPrint中

api = RedPrint(name='new_user', description='用户', api_doc=api_doc)

@api.route('/test', methods=["Get"])
@api.doc(auth=True)
def test_api():
    test_data={"test": "Hello, world."}
    new_user = NewUser.query.get_or_404(ident="10")
    return Success(data=new_user)

@api.route('/callbacktest', methods=['Get', 'POST'])
def callback_test():
    import random
    validator, request_data = BaseValidator().get_all_json(), BaseValidator().get_request_data()
    print(validator)
    callback = Callback()
    if "echostr" in validator:
        sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sEchoStr = \
            validator['msg_signature'], validator['timestamp'], validator['nonce'], validator["echostr"]
        res = callback.callback_validation(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sEchoStr, is_app=False)
        return res
    else:
        sReqData = request_data.decode("utf-8")
        sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce = \
            validator['msg_signature'], validator['timestamp'], validator['nonce']
        res = callback.callback_external_push(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sReqData)
        if isinstance(res, dict):
            user_list, change_type = res["user_list"], res["change_type"]
            if "chat_id" not in res:
                user_info = user_list[0]
                user_name = user_info["external_contact"]["name"]
                user_data = NewUser.query.filter(NewUser.nickname == user_name).first()
                if user_data:
                    user_cls = NewUser.get(nickname=user_name)
                    update_data = {
                        "is_in_contract": change_type
                    }
                    user_cls.update(**update_data)
            else:
                chat_id = res["chat_id"]
                if len(user_list) == 2:
                    user_name_0 = user_list[0]["external_contact"]["name"]
                    user_name_1 = user_list[1]["external_contact"]["name"]
                    time.sleep(3 + random.random())
                    update_dict = {
                        "group_id": chat_id,
                        "status": 2
                    }
                    print([user_name_0, user_name_1])
                    group_data = Group.query.filter(Group.group_id == chat_id).first()
                    if not group_data:
                        group_data_1 = Group.query.filter(
                            and_(Group.user_nickname == user_name_0, Group.shop_owner_nickname == user_name_1, Group.group_id=='')).order_by(Group.id.desc()).first()
                        group_data_2 = Group.query.filter(
                            and_(Group.user_nickname == user_name_1, Group.shop_owner_nickname == user_name_0, Group.group_id=='')).order_by(Group.id.desc()).first()
                        print(group_data_1)
                        print(group_data_2)
                        if group_data_1:
                            group_data_1.update(**update_dict)
                        elif group_data_2:
                            group_data_2.update(**update_dict)
                    else:
                        print(group_data)
                else:
                    group_data = Group.query.filter(Group.group_id == chat_id).first()
                    update_dict = {
                        "status": 1
                    }
                    if group_data:
                        group_data.update(**update_dict)
    return Success(0)

@api.route('/customservice', methods=['GET', 'POST'])
def custom_service():
    validator, request_data = BaseValidator().get_all_json(), BaseValidator().get_request_data()
    print(validator)
    callback = Callback()
    if "echostr" in validator:
        sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sEchoStr = \
            validator['signature'], validator['timestamp'], validator['nonce'], validator['echostr']
        res = callback.callback_validation(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sEchoStr)
        return res
    else:
        openid = validator["openid"]
        print(openid)
        time.sleep(1)
        user_data = NewUser.query.filter(NewUser.openid == openid).first()
        if user_data.extend:
            res = callback.callback_post_cs_message(openid, reply_type=user_data.extend)
        else:
            res = callback.callback_post_cs_message(openid, reply_type = 0)
        return "Success"



@api.route("/updateuser", methods=["POST"])
def add_user():
    validator = BaseValidator().get_all_json()
    print(validator)
    openid = validator["open_id"]
    session_key = validator["session_id"]
    if "encryptedData" in validator:
        print("start decrypt")
        encrypted_data = validator["encryptedData"]
        iv = validator["iv"]
        wx_token = WxToken("")
        res = wx_token.decryt(session_key, iv, encrypted_data)
        print(res)

    validator.pop("session_id")
    validator.pop("req_time")
    user_data = NewUser.query.filter(NewUser.openid==openid).first()
    # print(user_data)
    if user_data:
        user_cls = NewUser.get(openid=openid)
        new_user = user_cls.update(**validator)
    else:
        new_user = NewUser.create(**validator)

    return Success(data=new_user)

@api.route("/login", methods=["POST"])
def user_login():
    validator = BaseValidator().get_all_json()
    print(validator)
    ticket_code = validator["ticket_code"]
    print(ticket_code)
    wx_token = WxToken(ticket_code)
    wx_result = wx_token.get()
    open_id = wx_result["openid"]
    session["open_id"] = open_id
    session_id = wx_result["session_key"]
    user_data = NewUser.query.filter(NewUser.openid==open_id).first()
    if user_data:
        user = user_data
    else:
        user = {}
        add_data = {
            "openid": open_id
        }
        add_user_data = NewUser.create(**add_data)
    res = {
        "open_id": open_id,
        "session_id": session_id,
        "user": user
    }
    return Success(res)

@api.route("/joincontract", methods=["POST"])
def is_reqister():
    validator = BaseValidator().get_all_json()
    openid = validator["open_id"]
    is_in_contract = validator["is_in_contract"]
    user_data = NewUser.query.filter(NewUser.openid==openid).first()
    if user_data:
        update_data = {
            "is_in_contract": is_in_contract
        }
        user_data.update(**update_data)
    return Success({"res": "join success"})

@api.route("/mobile", methods=["POST"])
def store_mobile():
    validator = BaseValidator().get_all_json()
    openid = validator["open_id"]
    session_key = validator["session_id"]
    encrypted_data = validator["encrypted_data"]
    iv = validator["iv"]
    wx_token = WxToken("")
    mobile = wx_token.decryt(session_key, iv, encrypted_data)
    print(mobile)
    mobile = mobile["phoneNumber"]
    shop_data = Shop.query.filter(Shop.mobile==mobile).first()
    if shop_data:
        is_shop_owner = 1
        shop_id = shop_data.poi_id
    else:
        is_shop_owner = 0
        shop_id = "0"
    user_data = NewUser.query.filter(NewUser.openid==openid).first()
    if user_data:
        user_dict = {
            "mobile": mobile,
            "is_shop_owner": is_shop_owner,
            "shop_id": shop_id,
        }
        user_data.update(**user_dict)
    else:
        user_dict = {
            "open_id": openid,
            "mobile": mobile,
            "is_shop_owner": is_shop_owner,
            "shop_id": shop_id,
        }
        NewUser.create(**user_dict)
    return Success(user_dict)

@api.route("/isshopowner", methods=["POST"])
def is_shop_owner():
    validator = BaseValidator().get_all_json()
    mobile = validator["mobile"]
    print(mobile)
    shop_data = Shop.query.filter(Shop.mobile == mobile).all()
    if shop_data:
        shop_data_list = shop_data
        distance_list = [-1]*len(shop_data)
        group_data_dict = {}
        street_info_list = []
        for shop_item in shop_data:
            if shop_item.district:
                street_info_list.append(shop_item.district)
            else:
                street_info_list.append("中关村")
        print(street_info_list)
        shop_collection = ShopCollection()
        shop_collection.fill(shop_data_list, distance_list, group_data_dict, street_info_list)
        res = shop_collection.items[:-1]
    else:
        res = {"not_found": 1}
    return Success(data=res)

@api.route("/isincontract", methods=["POST"])
def is_in_contract():
    validator = BaseValidator().get_all_json()
    openid = validator["open_id"]
    user_data = NewUser.query.filter(NewUser.openid==openid).first()
    if user_data:
        res = {"is_in_contract": user_data.is_in_contract}
    else:
        res = {"is_in_contract": user_data.is_in_contract}
    return Success(data=res)


@api.route("/choosereply", methods=["POST"])
def choose_reply():
    validator = BaseValidator().get_all_json()
    openid = validator["open_id"]
    reply_type = validator["reply_type"]
    user_data = NewUser.query.filter(NewUser.openid==openid).first()
    if user_data:
        user_dict = {
            "extend": reply_type
        }
        user_data.update(**user_dict)
        res = {"res": 0}
    else:
        res = {"res": -1}
    return Success(data=res)

@api.route("/groupcount", methods=["POST"])
def group_count():
    validator = BaseValidator().get_all_json()
    poi_id = validator["poi_id"]
    group_count = Group.shop_group_count(poi_id)

    return Success({"shop_group_count": group_count})

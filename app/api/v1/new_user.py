# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2018/5/31.
  ↓↓↓ 普通用户接口 ↓↓↓
"""
from flask import g, session

from app.libs.enums import ScopeEnum
from app.libs.error_code import Success
from app.libs.redprint import RedPrint

from app.libs.token_auth import auth
from app.models.new_user import NewUser
from app.models.shop import Shop
from app.api_docs.v1 import user as api_doc  # api_doc可以引入
from app.validators.base import BaseValidator
from app.validators.forms import ChangePasswordValidator
from app.service.wx_token import WxToken
from app.service.callback import Callback
import time

__author__ = 'Allen7D'

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
        user_id, change_type = res["user_id"], res["change_type"]
        user_info = callback.get_external_user_info(user_id)
        #user_openid = callback.get_external_user_openid(user_id)
        user_name = user_info["external_contact"]["name"]
        user_data = NewUser.query.filter(NewUser.nickname == user_name).first()
        if user_data:
            user_cls = NewUser.get(nickname=user_name)
            update_data = {
                "is_in_contract": change_type
            }
            user_cls.update(**update_data)
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
        res = callback.callback_post_cs_message(openid)
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
    print(user_data)
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
    shop_data = Shop.query.filter(Shop.mobile==mobile).first()
    if shop_data:
        res = shop_data
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

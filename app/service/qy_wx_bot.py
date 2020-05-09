# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2018/6/22.
"""
from flask import current_app

from app.libs.error_code import WeChatException
from app.libs.httper import HTTP
import base64
from Crypto.Cipher import AES
import requests
import json

__author__ = "Allen7D"


class QyWxBot:
    """微信·小程序的Token获取(小程序登录)"""

    def __init__(self):
        self.group_chat_url = current_app.config["GROUP_CHAT_URL"]

    def add_group_chat(self, group_name, user_list=[]):
        post_url = self.group_chat_url + "addgroupchat"
        params = {
            "user_list": user_list,
            "group_name": group_name,
        }
        print(params)
        headers = {'Content-Type': 'application/json;charset=UTF-8'}
        r = requests.post(post_url, data=json.dumps(params).encode("utf-8"), headers=headers)
        self.__process_login_error(r.json())  # 微信异常处理
        return r.json()

    def awake_group(self, group_name):
        post_url = self.group_chat_url + "awakegroup"
        params = {
            "group_name": group_name
        }
        headers = {'Content-Type': 'application/json;charset=UTF-8'}
        r = requests.post(post_url, data=json.dumps(params).encode("utf-8"), headers=headers)
        self.__process_login_error(r.json())  # 微信异常处理
        return r.json()
    
    def __process_login_error(self, wx_result):
        if not wx_result:
            raise WeChatException()
        if "errcode" in wx_result.keys():
            raise WeChatException(
                msg=wx_result["errmsg"], error_code=wx_result["errcode"],
            )


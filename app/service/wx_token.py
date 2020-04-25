# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2018/6/22.
"""
from flask import current_app

from app.libs.error_code import WeChatException
from app.libs.httper import HTTP
import base64
from Crypto.Cipher import AES

__author__ = "Allen7D"


class WxToken:
    """微信·小程序的Token获取(小程序登录)"""

    def __init__(self, code):
        self.code = code
        self.wx_app_id = current_app.config["APP_ID"]
        self.wx_app_secret = current_app.config["APP_SECRET"]

    @property
    def wx_login_url(self):
        return current_app.config["LOGIN_URL"].format(
            self.wx_app_id, self.wx_app_secret, self.code
        )

    def get(self):
        print(self.wx_login_url)
        wx_result = HTTP.get(self.wx_login_url)
        print(wx_result)
        self.__process_login_error(wx_result)  # 微信异常处理
        return wx_result

    def decryt(self, session_key, iv, encrypted_data):
        import json

        session_key = base64.b64decode(session_key)
        encrypted_data = base64.b64decode(encrypted_data)
        iv = base64.b64decode(iv)
        cipher = AES.new(session_key, AES.MODE_CBC, iv)
        decrypted = json.loads(self._unpad(cipher.decrypt(encrypted_data)).decode())
        if decrypted['watermark']['appid'] != self.wx_app_id:
            raise Exception('Invalid Buffer')
        return decrypted


    def __process_login_error(self, wx_result):
        if not wx_result:
            raise WeChatException()
        if "errcode" in wx_result.keys():
            raise WeChatException(
                msg=wx_result["errmsg"], error_code=wx_result["errcode"],
            )

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

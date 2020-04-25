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


class QyWxToken:
    """微信·小程序的Token获取(小程序登录)"""

    def __init__(self):
        self.corp_id = current_app.config["CORP_ID"]
        self.corp_secret = current_app.config["CORP_SECRET"]
        self.access_token = ''
        self.corp_api_url = current_app.config["CORP_API_URL"]
        self.token_url = current_app.config["TOEN_URL"]

    def get_access_token(self):
        get_token_url = self.token_url.format()



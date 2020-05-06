# _*_ coding: utf-8 _*_

from flask import current_app

from app.libs.WXBizMsgCrypt3 import WXBizMsgCrypt
import xml.etree.cElementTree as ET
from app.libs.httper import HTTP

class Callback:
    def __init__(self):
        self.token = current_app.config["CALLBACK_TOKEN"]
        self.encoding_aes_key = current_app.config["CALLBACK_AESKEY"]
        self.corp_id = current_app.config["CORP_ID"]
        self.app_id = current_app.config["APP_ID"]
        self.app_secret = current_app.config["APP_SECRET"]
        self.access_token = ""


        self.get_access_token_url = current_app.config["GET_ACCESS_TOKEN"]
        self.post_cs_message = current_app.config["POST_CS_MESSAGE"]
        # self.contact_header_url = current_app.config["CONTACT_HEADER_URL"]
        self.media_list_url = current_app.config["MEDIA_LIST_URL"]
        self.contact_header_media_id = ""

        self.callback_access_token()
        # self.callback_media_id()
        self.media_id = "e6l0-nJTQCZSux6iPa4tQRaZO3p84b60HfwyRMiPKGoBY3rXwM4F6FxaH6zOpAts"
        # self.wxcpt = WXBizMsgCrypt(self.token, self.encoding_aes_key, self.corp_id)


    def callback_validation(self, verify_msg_sig, verify_time_stamp, verify_nonce, verify_echo_str, is_app=True):
        # wxcpt = WXBizMsgCrypt(self.token, self.encoding_aes_key, self.corp_id)
        # ret = wxcpt.VerifyAESKey()
        # print(ret)
        if is_app:
            wxcpt = WXBizMsgCrypt(self.token, self.encoding_aes_key, self.app_id)
            ret, sEchoStr = wxcpt.VerifyURLWechat(verify_msg_sig, verify_time_stamp, verify_nonce, verify_echo_str)
        else:
            wxcpt = WXBizMsgCrypt(self.token, self.encoding_aes_key, self.corp_id)
            ret, sEchoStr = wxcpt.VerifyURLWework(verify_msg_sig, verify_time_stamp, verify_nonce, verify_echo_str)
        if ret != 0:
            print("ERR: VerifyURL ret: " + str(ret))

        return sEchoStr

    def callback_external_push(self, sReqMsgSig, sReqTimeStamp, sReqNonce, sReqData):
        wxcpt = WXBizMsgCrypt(self.token, self.encoding_aes_key, self.corp_id)
        ret, sMsg = wxcpt.DecryptMsg(sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
        print(ret, sMsg)
        if (ret != 0):
            print("ERR: DecryptMsg ret: " + str(ret))
            # sys.exit(1)
        # 解密成功，sMsg即为xml格式的明文
        # TODO: 对明文的处理
        # For example:
        sMsg = sMsg.decode("utf-8")
        print(sMsg)
        xml_tree = ET.fromstring(sMsg)
        content = xml_tree.find("ExternalUserID").text
        print(content)
        return content

    def callback_access_token(self):
        get_url = self.get_access_token_url.format(self.app_id, self.app_secret)
        res = HTTP.get(get_url)
        self.access_token = res["access_token"]
        print("get access token")
        print(self.access_token)
        return 0

    def callback_media_id(self):
        post_url = self.media_list_url.format(self.access_token)
        print(post_url)
        params = {
            "type": "image",
            "offset": 0,
            "count": 10,
        }
        res = HTTP.post(post_url, params)
        print(res)


    def callback_post_cs_message(self, user_openid):
        post_url = self.post_cs_message.format(self.access_token)
        params = {
            "touser": user_openid,
            "msgtype": "text",
            "text":
            {
                "content": "请长按以下按钮添加企业通讯录为好友"
            }
        }
        res = HTTP.post(post_url, params)
        params = {
            "touser": user_openid,
            "msgtype": "image",
            "image":
                {
                    "media_id": self.media_id
                }
        }
        res = HTTP.post(post_url, params)
        return res




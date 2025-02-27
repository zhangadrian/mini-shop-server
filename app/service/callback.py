# _*_ coding: utf-8 _*_

from flask import current_app

from app.libs.WXBizMsgCrypt3 import WXBizMsgCrypt
from app.libs.httper import HTTP

import xml.etree.cElementTree as ET

from app.service.cache import cache

class Callback:
    def __init__(self):
        self.token = current_app.config["CALLBACK_TOKEN"]
        self.encoding_aes_key = current_app.config["CALLBACK_AESKEY"]
        self.corp_id = current_app.config["CORP_ID"]
        self.corp_secret = current_app.config["CORP_SECRET"]
        self.contact_secret = current_app.config["CONTACT_SECRET"]
        self.app_id = current_app.config["APP_ID"]
        self.app_secret = current_app.config["APP_SECRET"]
        self.access_token = ""
        self.access_token_qy = ""


        self.get_access_token_url = current_app.config["GET_ACCESS_TOKEN"]
        self.get_access_token_url_qy = current_app.config["TOKEN_URL"]
        self.post_cs_message = current_app.config["POST_CS_MESSAGE"]
        # self.contact_header_url = current_app.config["CONTACT_HEADER_URL"]
        self.media_list_url = current_app.config["MEDIA_LIST_URL"]
        self.corp_external_api_url = current_app.config["CORP_EXTERNAL_API_URL"]
        self.corp_contact_api_url = current_app.config["CORP_CONTACT_API_URL"]
        self.contact_header_media_id = ""

        self.callback_access_token()
        # self.callback_media_id()
        self.media_id_file_path = "/root/adhcczhang/mini-shop-server/app/static/media_id.pkl"
        #self.media_id = "jf4QPJt75KQP1HOUFdo1vbxmwt6QM5F1RL8Ol3ArvR_w9lwaEqfphIcGOtgy1RVD"
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
        sMsg = sMsg.decode("utf-8")
        xml_tree = ET.fromstring(sMsg)
        if xml_tree.find("ExternalUserID") != None:
            user_id = xml_tree.find("ExternalUserID").text
            change = xml_tree.find("ChangeType").text
            if 'del' in change:
                change_type = 0
            else:
                change_type = 1
            user_info = self.get_external_user_info(user_id, info_type="external")
            user_list = [user_info]
            res = {
                "user_list": user_list,
                "change_type": change_type,
                "external_user": 1
            }
            return res
        elif xml_tree.find("ChatId") != None:
            chat_id = xml_tree.find("ChatId").text
            res_dict = self.get_change_groupchat_info(chat_id)
            user_list, chat_id = res_dict["user_list"], res_dict["chat_id"]
            print(user_list)
            print(chat_id)
            res = {
                "user_list": user_list,
                "change_type": len(user_list),
                "chat_id": chat_id
            }
            return res
        elif xml_tree.find("ChangeType") != None:
            change_type = xml_tree.find("ChangeType").text
            if "update_user" in change_type:
                if xml_tree.find("Status") != None:
                    status = str(xml_tree.find("Status").text)
                    shop_id = xml_tree.find("UserID").text
                    res = {
                        "status": status,
                        "contact": 1,
                        "shop_id": shop_id
                    }
                    return res


    @cache.cached(timeout=6000, key_prefix='access_token')
    def callback_access_token(self):
        get_url = self.get_access_token_url.format(self.app_id, self.app_secret)
        res = HTTP.get(get_url)
        print("get access token")
        return res["access_token"]

    @cache.cached(timeout=6000, key_prefix='access_token_qy')
    def callback_access_token_qy(self):
        get_url = self.get_access_token_url_qy.format(self.corp_id, self.corp_secret)
        res = HTTP.get(get_url)
        print("get access token qy")
        return res["access_token"]

    @cache.cached(timeout=6000, key_prefix='access_token_contact')
    def callback_access_token_contact(self):
        get_url = self.get_access_token_url_qy.format(self.corp_id, self.contact_secret)
        res = HTTP.get(get_url)
        print("get access token contact")
        return res["access_token"]

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

    @cache.cached(timeout=36000, key_prefix="media_id")
    def get_media_id(self):
        import pickle
        with open(self.media_id_file_path, 'rb') as media_id_file:
            media_id = pickle.load(media_id_file)["media_id"]
        return media_id


    def callback_post_cs_message(self, user_openid, reply_type=0):
        media_id_list = self.get_media_id()
        intro_list = ["请长按以下按钮添加企业通讯录为好友", "请长按以下按钮添加微信工作台"]
        media_id = media_id_list[int(reply_type)]
        intro = intro_list[int(reply_type)]
        access_token = self.callback_access_token()
        print(access_token)
        post_url = self.post_cs_message.format(access_token)
        params = {
            "touser": user_openid,
            "msgtype": "text",
            "text":
            {
                "content": intro
            }
        }
        res = HTTP.post(post_url, params)
        params = {
            "touser": user_openid,
            "msgtype": "image",
            "image":
                {
                    "media_id": media_id
                }
        }
        res = HTTP.post(post_url, params)
        return res

    def get_external_user_info(self, user_id, info_type="external"):
        if info_type == "external":
            access_token_qy = self.callback_access_token_qy()
            get_url = self.corp_external_api_url.format("get", access_token_qy) + "&external_userid=" + user_id
            res = HTTP.get(get_url)
        else:
            access_token_qy = self.callback_access_token_contact()
            get_url = self.corp_contact_api_url.format("get", access_token_qy) + "&userid=" + user_id
            res = HTTP.get(get_url)
        print(res)
        return res

    def get_external_user_openid(self, user_id):
        access_token_qy = self.callback_access_token_qy()
        post_url = self.corp_external_api_url.format("convert_to_openid", access_token_qy)
        params = {
            "external_userid": user_id
        }
        res = HTTP.post(post_url, params)
        print(res)
        return res

    def get_change_groupchat_info(self, chat_id):
        access_token_qy = self.callback_access_token_qy()
        # print(access_token_qy)
        post_url = self.corp_external_api_url.format("groupchat/get", access_token_qy)
        # print(post_url)
        # print(chat_id)
        params = {
            "chat_id": chat_id
        }
        res = HTTP.post(post_url, params)
        # print(res)
        member_list = res["group_chat"]["member_list"]
        owner = res["group_chat"]["owner"]
        user_list = [0,0]
        for member in member_list:
            if member["type"] == 2:
                user_id = member["userid"]
                user_info = self.get_external_user_info(user_id, info_type="external")
                user_list[0] = user_info
            if member["type"] == 1 and member["userid"] != owner:
                user_id = member["userid"]
                user_info = self.get_external_user_info(user_id, info_type="shop_owner")
                user_list[1] = user_info
        res_dict = {
            "chat_id": res["group_chat"]["chat_id"],
            "user_list": user_list
        }
        return res_dict

    def get_user_status(self, user_id):
        access_token_qy = self.callback_access_token_contact()
        print(user_id)
        get_url = self.corp_contact_api_url.format("get", access_token_qy) + "&userid=" + user_id
        res = HTTP.get(get_url)
        print(res)
        if "status" not in res:
            res = {"status": 4}
        return res

    def change_remark(self, user_id, external_userid, remark):
        access_token_qy = self.callback_access_token_qy()
        post_url = self.corp_external_api_url.format("remark", access_token_qy)
        params = {
            "userid": user_id,
            "external_userid": external_userid,
            "remark": remark
        }
        res = HTTP.post(post_url, params)
        return res




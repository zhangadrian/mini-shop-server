# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2018/4/2.
"""
__author__ = 'Allen7D'

DEBUG = True

# Token 配置
SECRET_KEY = 'But you, Lord , are a shield around me, my glory, the One who lifts my head high.'  # 加密
TOKEN_EXPIRATION = 30 * 24 * 3600  # 有效期: 30天

# MySQL 数据库配置
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@localhost:3306/zerd?charset=utf8mb4'
SQLALCHEMY_ENCODING = 'utf-8'
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 屏蔽 sql alchemy 的 FSADeprecationWarning

# 微信·小程序
APP_ID = 'wxafc8a1a131f0eb7d'
APP_SECRET = '0b163686815e14682e43228ec19ce557'
LOGIN_URL = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'

# 企业微信
CORP_ID = 'ww43b2b04892bbeaed'
CORP_SECRET = 'T_-UpwhdUHc7qr6qTndWykJwudi_KoQafKnckUGS_tw'
CONTACT_SECRET = "xaoqOAXzX0vmm5skthDfm9K0PGgd3XSECAqi2vgSrlw"
TOKEN_URL = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}'
CORP_EXTERNAL_API_URL = 'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/{0}?access_token={1}'
CORP_CONTACT_API_URL = 'https://qyapi.weixin.qq.com/cgi-bin/user/{0}?access_token={1}'

# 回调函数TOKEN与AESKey
CALLBACK_TOKEN = "K0dBHVCzvRMIJMEn2qRQeO"
CALLBACK_AESKEY = "5qnmYF32XB0sMjXdiLmmmtdTVSGGjBiAs3t4J0CzkAJ"

# 客服会话URl
GET_ACCESS_TOKEN = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}"
POST_CS_MESSAGE = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}"
MEDIA_LIST_URL = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={0}"
QR_FILE_PATH = ""

# 操作URL
GROUP_CHAT_URL = 'http://ux94f4.natappfree.cc/v1/user/'

#腾讯云cos
COS_SECRET_ID = "AKIDnLyNWgfQ7WehY9TXUDfqwlJVRJumZjqg"
COS_SECRET_KEY = "oNr42kESPQL0nMespdZIlzmItEJBsGOX"

# 微信·开放平台(OPEN)登录[第三方(Third-Party)]
OPEN_APP_ID = 'wx87186e0123456789'
OPEN_APP_SECRET = '606d686fa91edc283d9cd00123456789'
OPEN_SCOPE = 'snsapi_login'
OPEN_STATE = '3d6be0a4035d839573b04816624a415e'
REDIRECT_URI = 'https%3a%2f%2fapi.ivinetrue.com%2ftoken%2fuser'
OPEN_AUTHORIZE_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={0}&redirect_uri={1}&response_type=code&scope={2}&state={3}#wechat_redirect'.format(
	OPEN_APP_ID, OPEN_APP_SECRET, OPEN_SCOPE, OPEN_STATE
)
OPEN_ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code'
OPEN_USER_INFO_URL = 'https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}&lang=zh_CN'

# 微信·公众平台(Account)·服务号登录
ACCOUNT_APP_ID = 'wx7bc53e1ab38e9f92'
ACCOUNT_APP_SECRET = 'c96c84b27ea4a353b10d7353b9cf5a09c'
REDIRECT_URI = 'https%3a%2f%2fwww.ivinetrue.com'

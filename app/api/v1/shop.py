# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2019/6/27.
  ↓↓↓ 管理员接口 ↓↓↓
"""
from app.libs.error_code import Success
from app.libs.redprint import RedPrint
from app.libs.token_auth import auth
from app.libs.poi_search.es_search import search
from app.models.base import db, Pagination
from app.models.shop import Shop
from app.models.new_user import NewUser
from app.service.qy_wx_bot import QyWxBot
from app.api_docs.v1 import shop as api_doc
from app.validators.base import BaseValidator
from app.validators.forms import PaginateValidator, ResetPasswordValidator
from time import time

__author__ = 'Allen7D'

api = RedPrint(name='shop', description='用户管理', api_doc=api_doc)


@api.route("/test", methods=["POST"])
def test_cms():
    res={
        "res": "Hello, world."
    }
    return Success(data=res)

@api.route('/list', methods=['POST'])
def get_list():
    '''获取用户列表(分页)'''
    print(1)
    validator = BaseValidator().get_all_json()
    print(validator)
    page = validator["page"]
    size = validator["size"]
    print(page)
    print(size)

    t1 = time()
    filter_key = "qqmap_14891966996318802388"
    mobile_key = 15245079525
    #paginator = Shop.query.paginate(page=page, per_page=size, error_out=False)
    #paginator = Shop.query.filter_by(id=10).first_or_404()
    #paginator = Shop.query.filter_by(mobile=mobile_key).all_or_404()
    paginator = Shop.query.limit(10).all()
    t2 = time()
    print(t2-t1)
    return Success(data=paginator)

@api.route('/searchshop', methods=['POST'])
def search_shop():
    validator = BaseValidator().get_all_json()
    keyword_str = validator['keyword']
    location = validator['location']
    page = validator['page']
    size = validator['size']
    t1 = time()
    search_res = search(location, keyword=[keyword_str])
    t2 = time()
    print(t2 -t1)
    print(search_res)
    filter_list = []
    for item in search_res:
        #print(type(item))
        filter_list.append(item['_source']['id'])
    #print(filter_list)

    shop_data_list = Shop.query.filter(Shop.poi_id.in_(filter_list)).paginate(page=page, per_page=size, error_out=False)
    t3 = time()
    print(t3 - t2)
    res = {
        "total": shop_data_list.total,
        "current_page": shop_data_list.page,
        "items":shop_data_list.items
    }
    return Success(data=res)

@api.route('/test_filter', methods=['POST'])
def get_one():
    '''获取用户信息'''
    validator = BaseValidator().get_all_json()
    filter_list = []
    for i in range(100):
        filter_list.append(str(i-2))
    page = validator["page"]
    size = validator["size"]
    print(filter_list)
    t1 = time()
    u1 = Shop.query.filter(Shop.poi_id.in_(filter_list)).paginate(page=0, per_page=size, error_out=False)
    res = {
        "total": u1.total,
        "current_page": u1.page,
        "items": u1.items
    }

    return Success(res)

@api.route('/creategroup', methods=['POST'])
def create_group():
    import requests
    import json
    validator = BaseValidator().get_all_json()
    shop_id = validator["poi_id"]
    user_id = validator["open_id"]
    print(shop_id)
    print(user_id)
    shop_owner_data = NewUser.query.filter(NewUser.shop_id==shop_id).first()
    user_data = NewUser.query.filter(NewUser.openid==user_id).first()
    print(shop_owner_data)
    print(user_data)
    if shop_owner_data:
        shop_owner_name = shop_owner_data.nickname
    user_name = user_data.nickname
    
    #user_list = [shop_owner_name, user_name]
    if shop_owner_data.is_in_contract == 1:
        user_list = ["Adrian", user_name]
        qy_wx_bot = QyWxBot()
        res = qy_wx_bot.add_group_chat(user_list=user_list)
        return Success({"create_group": 1})
    else:
        return Success({"create_group": -1})




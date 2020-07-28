# _*_ coding: utf-8 _*_

from app.libs.error_code import Success
from app.libs.redprint import RedPrint
from app.service.shop_recall import Recall
from app.models.new_shop import NewShop as Shop
from app.models.shop_detail import ShopDetail
from app.models.group import Group
from app.api_docs.v1 import shop as api_doc
from app.validators.base import BaseValidator
from app.model_views.shop import ShopDetailView
from app.service.tencent_cos import TencentCos
from time import time

__author__ = 'adhcczhang'

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

@api.route('/searchshop', methods=['POST'])
def search_shop():
    validator = BaseValidator().get_all_json()
    user_id = validator["open_id"]
    keyword_str = validator['keyword']
    location = validator['location']
    page = validator['page']
    size = validator['size']
    if "category" in validator:
        category = validator["category"]
    else:
        category = ""
    recall = Recall()
    res = recall.sort_by_distance(page, size, keyword_str, location, user_id, category)
    return Success(data=res)


@api.route('/groupshopinfo', methods=['POST'])
def group_shop_info():
    validator = BaseValidator().get_all_json()
    shop_id_list = validator["poi_id_list"]
    user_id = validator["open_id"]
    res = Group.get_shop_list(user_id, shop_id_list)
    return Success({"created_group_shop": res})


@api.route('/updateshopdetail', methods=['POST'])
def update_shop_detail():
    validator = BaseValidator().get_all_json()
    poi_id = validator["poi_id"]
    update_data = validator["update_data"]

    new_shop_detail = ShopDetail.update_shop_detail(poi_id, update_data)
    return Success(new_shop_detail)
    # return Success({"res": 0})

@api.route('/updateshopinfo', methods=['POST'])
def update_shop_info():
    validator = BaseValidator().get_all_json()
    poi_id = validator["poi_id"]
    update_data = validator["update_data"]

    new_shop_info = Shop.update_shop_info(poi_id, update_data)
    return Success(new_shop_info)
    # return Success({"res": 0})


@api.route('/deleteshopdetail', methods=['POST'])
def delete_shop_detail():
    validator = BaseValidator().get_all_json()
    poi_id = validator["poi_id"]
    update_data = validator["update_data"]

    new_shop_detail = ShopDetail.delete_shop_detail(poi_id, update_data)
    shop = Shop.query.filter(Shop.poi_id == poi_id).first()
    shop_detail_view = ShopDetailView(shop, new_shop_detail)
    return Success(shop_detail_view)
    # return Success({"res": 0})

# TODO
@api.route('/uploadactiondata', methods=['POST'])
def upload_action_data():
    return Success({"res": 0})


@api.route('/getshopdetailinfo', methods=["POST"])
def get_shop_detail_info():
    validator = BaseValidator().get_all_json()
    poi_id = validator["poi_id"]
    shop = Shop.query.filter(Shop.poi_id == poi_id).first()
    shop_detail = ShopDetail.query.filter(ShopDetail.poi_id == poi_id).first()
    shop_detail_view = ShopDetailView(shop, shop_detail)

    return Success(data=shop_detail_view)

@api.route('/getcoscredential', methods=["POST"])
def get_cos_credential():
    tencent_cos = TencentCos()
    cos_credential = tencent_cos.get_credential()

    return Success(data=cos_credential)

@api.route('/claimshop', methods=["POST"])
def claim_shop():
    validator = BaseValidator().get_all_json()
    poi_id_list = validator["poi_id_list"]
    Shop.claim_shop(poi_id_list)
    return Success({"res": 0})


# TODO
@api.route('/inviteshopowner', methods=['POST'])
def invite_shop_owner():
    return Success({"res": 0})






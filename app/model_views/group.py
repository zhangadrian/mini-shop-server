# _*_ coding: utf-8 _*_
from app.model_views.base import ModelView
from app.model_views.shop import BaseShopCollection
from app.models.new_shop import NewShop as Shop
__author__ = "adhcczhang"


class BaseGroupView(ModelView):
    fields = ["group_name", "user_nickname", "shop_owner_nickname", "group_id", "poi_id"]

    def __init__(self, group, shop_info):
        self.group_name = group.group_name
        self.user_nickname = group.user_nickname
        self.shop_owner_nickname = group.shop_owner_nickname
        self.group_id = group.group_id
        self.poi_id = group.poi_id
        self.shop_info = shop_info


class GroupCollection:
    def __init__(self):
        self.items = []

    def get_shop_list(self, group_list):
        shop_id_list = []
        for group in group_list:
            shop_id_list.append(group.poi_id)
        shop_data_list = Shop.get_shop_info_list(shop_id_list)
        base_shop_collection = BaseShopCollection()
        shop_info_list = base_shop_collection.fill(shop_data_list)
        return shop_info_list

    def fill(self, group_list):
        shop_info_list = self.get_shop_list(group_list)
        zip_group_shop = zip(group_list, shop_info_list)
        self.items = [BaseGroupView(group_item, shop_item) for group_item, shop_item in zip_group_shop]
        return self.items



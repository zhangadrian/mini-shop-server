# _*_ coding: utf-8 _*_
from app.model_views.base import ModelView

__author__ = "adhcczhang"


class ShopViewModel(ModelView):
    fields = ["poi_id", "name", "address", "mobile", "latitude", "longitude", "distance", "group_created", "street_name"]

    def __init__(self, shop, distance, group_data_dict, street_name):
        self.name = shop.name
        self.address = shop.address
        self.mobile = shop.mobile
        self.poi_id = shop.poi_id
        self.latitude = shop.latitude
        self.longitude = shop.longitude
        self.distance = distance
        if self.poi_id in group_data_dict:
            self.group_created = 1
        else:
            self.group_created = 0
        self.street_name = street_name


class ShopCollection:
    def __init__(self):
        self.items = []

    def fill(self, shop_list, distance_list, group_data_dict, street_info_list):
        self.items = [ShopViewModel(shop_list[i], distance_list[i], group_data_dict, street_info_list[i]) for i in range(len(shop_list))]
        self.items.sort(key=lambda x:x.distance)


# _*_ coding: utf-8 _*_
from app.model_views.base import ModelView

__author__ = "adhcczhang"


class ShopViewModel(ModelView):
    fields = ["poi_id", "name", "address", "mobile", "latitude", "longitude", "distance"]

    def __init__(self, shop, distance, group_data_dict):
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


class ShopCollection:
    def __init__(self):
        self.items = []

    def fill(self, shop_list, distance_list, group_data_dict):
        print(type(shop_list.items))
        self.items = [ShopViewModel(shop_list.items[i], distance_list[i], group_data_dict) for i in range(len(shop_list.items))]


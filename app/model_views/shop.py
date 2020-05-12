# _*_ coding: utf-8 _*_

__author__ = "adhcczhang"


class ShopViewModel:
    def __init__(self, shop, distance):
        self.name = shop.name
        self.address = shop.address
        self.mobile = shop.mobile
        self.poi_id = shop.poi_id
        self.latitude = shop.latitude
        self.longitude = shop.longitude
        self.distance = distance


class ShopCollection:
    def __init__(self):
        self.items = []

    def fill(self, shop_list, distance_list):
        self.items = [ShopViewModel(shop_list.items[i], distance_list[i]) for i in range(len(shop_list.items))]

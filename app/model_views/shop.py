# _*_ coding: utf-8 _*_
from app.model_views.base import ModelView

__author__ = "adhcczhang"


class ShopViewModel(ModelView):
    fields = ["poi_id", "name", "address", "mobile", "latitude", "longitude", "distance",
              "group_created", "street_name", "category"]

    def __init__(self, shop, distance, group_data_dict, street_name, category):
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
        self.category = category


class ShopCollection:
    def __init__(self):
        self.items = []

    def change_category(self, category):
        category_list = category.split(":")
        if category_list[0] == "购物":
            if len(category_list) >= 2:
                if category_list[1] == "便利店" or category_list[1] == "超市":
                    return "购物"
        if category_list[0] == "美食":
            return "美食"
        if category_list[0] == "酒店宾馆":
            return "住宿"
        if category_list[0] == "汽车" or category_list[0] == "生活服务" or category_list[0] == "娱乐休闲":
            return "服务"
        if category_list[0] == "运动健身":
            return "健身"
        return "其他"

    def fill(self, shop_list, distance_list, group_data_dict, street_info_list):
        category_list = []
        for shop_data in shop_list:
            try:
                category = shop_data.category
                category_list.append(self.change_category(category))
            except:
                category_list.append("美食")
        self.items = [ShopViewModel(shop_list[i], distance_list[i], group_data_dict, street_info_list[i], category_list[i]) for i in range(len(shop_list))]
        self.items.sort(key=lambda x:x.distance)


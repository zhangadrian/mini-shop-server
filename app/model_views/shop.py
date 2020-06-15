# _*_ coding: utf-8 _*_
from app.model_views.base import ModelView
from app.models.new_shop import NewShop as Shop

import re

__author__ = "adhcczhang"


class ShopViewModel(ModelView):
    fields = ["poi_id", "name", "address", "mobile", "latitude", "longitude", "distance",
              "group_created", "street_name", "category", "business_hour"]

    def __init__(self, shop, distance, group_data_dict, street_name, category):
        self.name = shop.name
        self.address = shop.address
        self.mobile = shop.mobile
        self.poi_id = shop.poi_id
        self.latitude = shop.latitude
        self.longitude = shop.longitude
        self.business_hour = self.re_week(shop.businesshour)
        self.distance = distance
        if self.poi_id in group_data_dict:
            self.group_created = 1
        else:
            self.group_created = 0
        self.street_name = street_name
        self.category = category
    
    @staticmethod
    def re_week(s):
        if not s:
            return {"business_week": "周一至周日",
                    "business_hour": "00:00-23:59"}
        week_res_list = re.findall(r"(周[\u4e00-\u9fa5]{2}周[\u4e00-\u9fa5]{1})", s)
        time_res_list = re.findall(r"(\d{2}:\d{2}-\d{2}:\d{2})", s)
        if len(week_res_list) > 0:
            week_res = week_res_list[0]
        else:
            week_res = "周一至周日"

        if len(time_res_list) > 0:
            start_time = time_res_list[0].split("-")[0]
            end_time = time_res_list[-1].split("-")[1]
            time_res = start_time + "-" + end_time
        else:
            time_res = "00:00-23:59"
            
        return {"business_week": week_res,
                "business_hour": time_res}


class ShopCollection:
    def __init__(self):
        self.items = []
        self.debug = True

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
                category_list.append("其他")
        self.items = [ShopViewModel(shop_list[i], distance_list[i], group_data_dict, street_info_list[i], category_list[i]) for i in range(len(shop_list))]
        if self.debug:
            test_shop_data = Shop.query.filter(Shop.poi_id == "warrenyang_shop").first()
            test_shop_view = ShopViewModel(test_shop_data, 10, group_data_dict, "中关村", "美食")
            self.items.append(test_shop_view)
        self.items.sort(key=lambda x:x.distance)


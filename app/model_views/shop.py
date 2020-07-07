# _*_ coding: utf-8 _*_
from app.model_views.base import ModelView
from app.models.new_shop import NewShop as Shop

import re

__author__ = "adhcczhang"


class BaseShopView(ModelView):
    def __init__(self, shop):
        self.name = shop.name
        self.address = shop.address
        self.mobile = shop.mobile
        self.poi_id = shop.poi_id
        self.latitude = shop.latitude
        self.longitude = shop.longitude
        self.business_hour = self.re_week(shop.businesshour)
        try:
            self.category = self.change_category(shop.category)
        except:
            self.category = "更多"

    @staticmethod
    def str2weeklist(input):
        num_week_dict = {
            "周一": 0,
            "周二": 1,
            "周三": 2,
            "周四": 3,
            "周五": 4,
            "周六": 5,
            "周日": 6,
        }

        week_list = ["周一", "周二", "周三", "周四", "周五", "周六", "周日", ]

        try:
            start_weekday, end_weekday = input.split("至")
        except:
            start_weekday, end_weekday = "周一", "周日"

        start_index, end_index = num_week_dict[start_weekday], num_week_dict[end_weekday]

        try:
            res = week_list[start_index: end_weekday + 1]
        except:
            res = week_list
        return res

    def re_week(self, s):

        if not s:
            return {"business_week": self.str2weeklist("周一至周日"),
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

        return {"business_week": self.str2weeklist(week_res),
                "business_hour": time_res
                }

    def change_category(self, category):
        category_list = category.split(":")
        if category_list[0] == "购物":
            if len(category_list) >= 2:
                if category_list[1] == "便利店" or category_list[1] == "超市":
                    return "购物"
        if category_list[0] == "美食":
            return "餐饮"
        if category_list[0] == "酒店宾馆":
            return "住宿"
        if category_list[0] == "娱乐休闲":
            return "娱乐"
        if category_list[0] == "运动健身" or category_list[0] == "汽车" or category_list[0] == "生活服务":
            return "生活"
        return "更多"


class ShopViewModel(BaseShopView):
    fields = ["poi_id", "name", "address", "mobile", "latitude", "longitude", "distance",
              "group_created", "street_name", "category", "business_hour"]

    def __init__(self, shop, distance, group_data_dict, street_name):
        super(ShopViewModel, self).__init__(shop)
        self.distance = distance
        if self.poi_id in group_data_dict:
            self.group_created = 1
        else:
            self.group_created = 0
        self.street_name = street_name


class ShopDetailView(BaseShopView):
    fields = ["poi_id", "name", "address", "mobile", "category", "business_hour",
              "shop_pic_list", "shop_head_pic", "shop_intro", "shop_pic_comment_list"]

    def __init__(self, shop, shop_detail):
        super(ShopDetailView, self).__init__(shop)
        if shop_detail:
            self.shop_head_pic = shop_detail.shop_head_pic
            self.shop_intro = shop_detail.shop_intro
            self.shop_pic_list, self.shop_pic_comment_list = self.pic_list(shop_detail)
        else:
            self.shop_head_pic = ""
            self.shop_intro = ""
            self.shop_pic_list, self.shop_pic_comment_list = [], []


    def pic_list(self, shop_detail):
        shop_pic_list = [shop_detail.shop_pic_1,
                         shop_detail.shop_pic_2,
                         shop_detail.shop_pic_3,
                         shop_detail.shop_pic_4,
                         ]
        shop_pic_comment_list = [shop_detail.shop_pic_comment_1,
                                 shop_detail.shop_pic_comment_2,
                                 shop_detail.shop_pic_comment_3,
                                 shop_detail.shop_pic_comment_4,
                                ]
        return shop_pic_list, shop_pic_comment_list


class ShopCollection:
    def __init__(self):
        self.items = []
        self.debug = True

    def fill(self, shop_list, distance_list, group_data_dict, street_info_list):
        self.items = [ShopViewModel(shop_list[i], distance_list[i], group_data_dict, street_info_list[i]) for i in range(len(shop_list))]
        if self.debug:
            test_shop_data = Shop.query.filter(Shop.poi_id == "warrenyang_shop").first()
            test_shop_view = ShopViewModel(test_shop_data, 10, group_data_dict, "中关村")
            test_shop_view.category = "餐饮"
            self.items.append(test_shop_view)
        self.items.sort(key=lambda x:x.distance)


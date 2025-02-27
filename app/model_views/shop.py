# _*_ coding: utf-8 _*_
from app.model_views.base import ModelView
from app.models.new_shop import NewShop as Shop
from app.model_views.shop_detail import BaseShopDetailView

import re

__author__ = "adhcczhang"


class BaseShopView(ModelView):
    fields = ["poi_id", "name", "address", "mobile", "latitude", "longitude",
              "category", "business_hour", "shop_head_pic", "shop_intro", "status", "is_claimed"]

    def __init__(self, shop):
        self.name = shop.name
        self.address = shop.address
        self.poi_id = shop.poi_id
        self.latitude = shop.latitude
        self.longitude = shop.longitude
        self.shop_intro = shop.shop_intro
        self.is_claimed = shop.is_claimed
        self.shop_head_pic = shop.shop_head_pic
        self.business_hour = self.re_week(shop.businesshour)
        if shop.status:
            self.status = int(shop.status)
        else:
            self.status = 4

        if shop.new_mobile:
            self.mobile = shop.new_mobile
        else:
            self.mobile = shop.mobile

        try:
            self.category = self.change_category(shop.category)
        except:
            self.category = "更多"

    @staticmethod
    def str2weeklist(input):
        if "至" in input:
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
        else:
            res = input.split("到")
            return res

    @staticmethod
    def str2shortweeklist(input):
        if "至" in input:
            res = input
            return res
        else:
            res = []
            week_list = input.split("到")
            num_week_dict = {
                "周一": 0,
                "周二": 1,
                "周三": 2,
                "周四": 3,
                "周五": 4,
                "周六": 5,
                "周日": 6,
            }
            num_week_list = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
            week_num_list = []
            for week in week_list:
                week_num_list.append(num_week_dict[week])
            week_num_list.append(8)
            week_num_list.sort()
            print(week_num_list)
            start_index = week_num_list[0]
            res_list = []
            for i in range(1, len(week_num_list)):
                if week_num_list[i] - week_num_list[i - 1] > 1:
                    end_index = week_num_list[i - 1]
                    res_list.append([start_index, end_index])
                    start_index = week_num_list[i]
                    print(res_list)
            if len(res_list) == 0:
                res_list.append([start_index, start_index])
            for item in res_list:
                start_index, end_index = item
                if end_index - start_index > 0:
                    res.append(num_week_list[start_index] + "至" + num_week_list[end_index])
                else:
                    res.append(num_week_list[start_index])

            return res

    def re_week(self, s):

        if not s:
            return {"business_week": self.str2weeklist("周一至周日"),
                    "business_hour": "00:00-23:59"}
        # week_res_list = re.findall(r"(周[\u4e00-\u9fa5]{2}周[\u4e00-\u9fa5]{1})", s)
        week_res_list = re.findall(r"周[\u4e00-\u9fa5]*", s)
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
                "business_hour": time_res,
                "short_business_week": self.str2shortweeklist(week_res),
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
              "group_created", "street_name", "category", "business_hour", "shop_head_pic", "shop_intro", "status", "is_claimed", "is_user_shop"]

    def __init__(self, shop, distance, group_data_dict, street_name, user_id=""):
        super(ShopViewModel, self).__init__(shop)
        self.distance = distance
        if self.poi_id in group_data_dict:
            self.group_created = 1
        else:
            self.group_created = 0
        self.street_name = street_name
        if shop.user_id == user_id:
            self.is_user_shop = 1
        else:
            self.is_user_shop = 0


class ShopDetailView(BaseShopView, BaseShopDetailView):
    fields = ["poi_id", "name", "address", "mobile", "category", "business_hour",
              "shop_pic_list", "shop_head_pic", "shop_intro", "shop_pic_comment_list"]

    def __init__(self, shop, shop_detail):
        BaseShopView.__init__(self, shop)
        BaseShopDetailView.__init__(self, shop_detail)

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
    def __init__(self, is_debug=False):
        self.items = []
        self.debug = is_debug

    def fill(self, shop_list, distance_list, group_data_dict, street_info_list, user_id="0"):
        self.items = [ShopViewModel(shop_list[i], distance_list[i], group_data_dict, street_info_list[i], user_id) for i in range(len(shop_list))]
        if self.debug:
            test_shop_data = Shop.query.filter(Shop.poi_id == "Ceshihao").first()
            test_shop_view = ShopViewModel(test_shop_data, 10, group_data_dict, "中关村", user_id)
            test_shop_view.category = "餐饮"
            self.items.append(test_shop_view)
            # test_shop_data = Shop.query.filter(Shop.poi_id == "haolin_shop").first()
            # test_shop_view = ShopViewModel(test_shop_data, 10, group_data_dict, "中关村", user_id)
            # test_shop_view.category = "娱乐"
            # self.items.append(test_shop_view)
        self.items.sort(key=lambda x:x.distance)


class BaseShopCollection:
    def __init__(self):
        self.items = []

    def fill(self, shop_list):
        self.items = [BaseShopView(shop_item) for shop_item in shop_list]
        return self.items

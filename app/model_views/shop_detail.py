# _*_ coding: utf-8 _*_
from app.model_views.base import ModelView

__author__ = "adhcczhang"

class BaseShopDetailView(ModelView):
    fields = ["poi_id", "shop_pic_list", "shop_pic_index", "shop_pic_comment_list", "shop_pic_comment_index"]

    def __init__(self, shop_detail):
        print(shop_detail)
        if shop_detail:
            shop_detail_list_dict = self.dict2list(shop_detail)
            self.poi_id = shop_detail.poi_id
            self.shop_pic_list = shop_detail_list_dict["shop_pic_list"]
            self.shop_pic_index = shop_detail_list_dict["shop_pic_index"]
            self.shop_pic_comment_list = shop_detail_list_dict["shop_pic_comment_list"]
            self.shop_pic_comment_index = shop_detail_list_dict["shop_pic_comment_index"]
        else:
            self.poi_id = -1
            self.shop_pic_list = []
            self.shop_pic_index = []
            self.shop_pic_comment_list = []
            self.shop_pic_comment_index = []

    @staticmethod
    def row2dict(row):
        res = {}
        for column in row.__table__.columns:
            res[column.name] = str(getattr(row, column.name))
        return res

    def dict2list(self, shop_detail):
        pic_id_dict = {
            0: "shop_pic_1",
            1: "shop_pic_2",
            2: "shop_pic_3",
            3: "shop_pic_4",
        }

        comment_id_dict = {
            0: "shop_pic_comment_1",
            1: "shop_pic_comment_2",
            2: "shop_pic_comment_3",
            3: "shop_pic_comment_4",
        }
        shop_detail_dict = self.row2dict(shop_detail)
        shop_pic_list = []
        shop_pic_index = []
        shop_pic_comment_list = []
        shop_pic_comment_index = []
        for id in pic_id_dict:
            if shop_detail_dict[pic_id_dict[id]] != "":
                shop_pic_list.append(shop_detail_dict[pic_id_dict[id]])
                shop_pic_index.append(id)
                shop_pic_comment_list.append(shop_detail_dict[comment_id_dict[id]])
                shop_pic_comment_index.append(id)
        return {
            "shop_pic_list": shop_pic_list,
            "shop_pic_index": shop_pic_index,
            "shop_pic_comment_list": shop_pic_comment_list,
            "shop_pic_comment_index": shop_pic_comment_index,
        }



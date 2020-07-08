# _*_ coding: utf-8 _*_

from sqlalchemy import Column, Integer, String

from app.models.base import Base

__author__ = "adhcczhang"

class ShopDetail(Base):
    __tablename__ = "shop_detail"
    id = Column(Integer, primary_key=True, autoincrement=True)
    poi_id = Column(String(50), unique=True, comment="店铺ID")
    shop_head_pic = Column(String(1000), default="")
    shop_intro = Column(String(1000), default="")
    shop_pic_1 = Column(String(1000), default="")
    shop_pic_2 = Column(String(1000), default="")
    shop_pic_3 = Column(String(1000), default="")
    shop_pic_4 = Column(String(1000), default="")
    shop_pic_comment_1 = Column(String(1000), default="")
    shop_pic_comment_2 = Column(String(1000), default="")
    shop_pic_comment_3 = Column(String(1000), default="")
    shop_pic_comment_4 = Column(String(1000), default="")

    fields = [
        "id",
        "poi_id",
        "shop_head_pic",
        "shop_intro",
        "shop_pic_1",
        "shop_pic_2",
        "shop_pic_3",
        "shop_pic_4",
        "shop_pic_comment_1",
        "shop_pic_comment_2",
        "shop_pic_comment_3",
        "shop_pic_comment_4",
    ]

    def keys(self):
        self.hide("id")
        return self.fields

    @classmethod
    def update_shop_detail(cls, poi_id, update_data):
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
        shop_detail = cls.query.filter(cls.poi_id == poi_id).first()

        try:
            shop_pic_list = update_data["shop_pic_list"]
            shop_pic_index = update_data["shop_pic_index"]
        except:
            shop_pic_list = []
            shop_pic_index = []
        try:
            shop_pic_comment_list = update_data["shop_pic_comment_list"]
            shop_pic_comment_index = update_data["shop_pic_comment_index"]
        except:
            shop_pic_comment_list = []
            shop_pic_comment_index = []
        shop_detail_data = {"poi_id": poi_id}

        if "shop_head_pic" in update_data:
            shop_detail_data["shop_head_pic"] = update_data["shop_head_pic"]
        if "shop_intro" in update_data:
            shop_detail_data["shop_intro"] = update_data["shop_intro"]

        for index, pic in enumerate(shop_pic_list):
            update_index = shop_pic_index[index]
            shop_detail_data[pic_id_dict[update_index]] = pic

        for index, comment in enumerate(shop_pic_comment_list):
            update_index = shop_pic_comment_index[index]
            shop_detail_data[comment_id_dict[update_index]] = comment

        if shop_detail:
            shop_detail.update(**shop_detail_data)
        else:
            ShopDetail.create(**shop_detail_data)

        return shop_detail

    @classmethod
    def delete_shop_detail(cls, poi_id, delete_id_list):
        shop_detail = cls.query.filter(cls.poi_id == poi_id).first_or_404()
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

        update_data = {}
        for delete_id in delete_id_list:
            update_data[pic_id_dict[delete_id]] = ""
            update_data[comment_id_dict[delete_id]] = ""

        shop_detail.update(**update_data)

        return shop_detail

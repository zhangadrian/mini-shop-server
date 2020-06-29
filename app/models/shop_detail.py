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
        shop_detail = cls.query.filter(cls.poi_id == poi_id).first_or_404()
        shop_detail.update(**update_data)

        return shop_detail

    @classmethod
    def delete_shop_detail(cls, poi_id, delete_id_list):
        shop_detail = cls.query.filter(cls.poi_id == poi_id).first_or_404()
        pic_id_dict = {
            "0": "shop_pic_1",
            "1": "shop_pic_2",
            "2": "shop_pic_3",
            "3": "shop_pic_4",
        }

        word_id_dict = {
            "0": "shop_pic_comment_1",
            "1": "shop_pic_comment_2",
            "2": "shop_pic_comment_3",
            "3": "shop_pic_comment_4",
        }

        update_data = {}
        for delete_id in delete_id_list:
            update_data[pic_id_dict[delete_id]] = ""
            update_data[word_id_dict[delete_id]] = ""

        shop_detail.update(**update_data)

        return shop_detail

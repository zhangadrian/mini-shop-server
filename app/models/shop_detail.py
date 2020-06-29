# _*_ coding: utf-8 _*_

from sqlalchemy import Column, Integer, SmallInteger, String, Float, Text

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
    def update_shop_detal(cls, poi_id, update_data):
        shop_detail = cls.query.filter(cls.poi_id == poi_id).first_or_404()
        shop_detail.update(**update_data)

        return shop_detail


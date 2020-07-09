# _*_ coding: utf-8 _*_

from sqlalchemy import Column, Integer, SmallInteger, String, Float, Text

from app.models.base import Base

__author__ = "adhcczhang"


class NewShop(Base):
    __tablename__ = "shop_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    poi_id = Column(String(50), unique=True, comment="店铺ID")
    name = Column(String(100), comment="店铺名称")
    address = Column(String(500), comment="店铺地址")
    mobile = Column(String(50), comment="店铺电话")
    latitude = Column(Integer, comment="维度")
    longitude = Column(Integer, comment="经度")
    province = Column(String(50), comment="经度")
    rate = Column(Float, comment="评分")
    quality = Column(Float)
    category = Column(String(50))
    city = Column(String(50))
    poi_score = Column(Float)
    recommend = Column(String(1000))
    district = Column(String(50))
    businesshour = Column(String(1000))
    special = Column(String(1000))
    special_food = Column(String(1000))
    shop_head_pic = Column(String(1000), default="")
    shop_intro = Column(String(1000), default="")
    fields = [
        "poi_id",
        "name",
        "address",
        "mobile",
        "latitude",
        "longitude",
        "province",
        "rate",
        "quality",
        "category",
        "city",
        "poi_score",
        "recommend",
        "district",
        "businesshour",
        "special",
        "special_food",
        "shop_head_pic",
        "shop_intro",
    ]

    def keys(self):
        self.hide("id")
        return self.fields

    @classmethod
    def update_shop_info(cls, poi_id, update_data):
        shop_info = cls.query.filter(cls.poi_id == poi_id).first_or_404()

        if "businesshour" in update_data:
            businesshour = update_data["businesshour"]
            businessweek = update_data["businessweek"]
            new_businessweek = "到".join(businessweek)
            new_businesshour = businesshour + "\t" + new_businessweek
            update_data["businesshour"] = new_businesshour
            update_data.pop("businessweek")
        shop_info.update(**update_data)

        return shop_info

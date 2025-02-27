# _*_ coding: utf-8 _*_

from sqlalchemy import Column, Integer, SmallInteger, String, Float
from app.libs.poi_search.es_index_category import update_specific_index

from app.models.base import Base

__author__ = "adhcczhang"


class NewShop(Base):
    __tablename__ = "shop_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    poi_id = Column(String(50), unique=True, comment="店铺ID")
    user_id = Column(String(100), comment="店主ID")
    name = Column(String(100), comment="店铺名称")
    address = Column(String(500), comment="店铺地址")
    mobile = Column(String(50), comment="店铺电话")
    new_mobile = Column(String(50), comment="店铺电话")
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
    is_claimed = Column(SmallInteger, comment="是否已经认领", default=0)
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
        "is_claim",
    ]

    def keys(self):
        self.hide("id")
        return self.fields

    @classmethod
    def update_shop_info(cls, poi_id, update_data):
        shop_info = cls.query.filter(cls.poi_id == str(poi_id)).first_or_404()

        if "businesshour" in update_data:
            businesshour = update_data["businesshour"]
            businessweek = update_data["businessweek"]
            new_businessweek = "到".join(businessweek)
            new_businesshour = businesshour + "\t" + new_businessweek
            update_data["businesshour"] = new_businesshour
            update_data.pop("businessweek")
        shop_info.update(**update_data)
        cls.update_search_index(poi_id, update_data)
        return shop_info

    @staticmethod
    def update_search_index(poi_id, update_data):
        key_dict = {
            "name": 1,
            "address": 1,
            "mobile": 1,
        }

        index_dict = {}
        for key in key_dict:
            if key in update_data:
                index_dict[key] = update_data[key]
        if len(index_dict.keys()) > 0:
            update_specific_index(poi_id, index_dict)
        return 0


    @classmethod
    def get_shop_info_list(cls, shop_id_list):
        shop_data_list = NewShop.query.filter(NewShop.poi_id.in_(shop_id_list)).all()
        return shop_data_list

    @classmethod
    def claim_shop(cls, poi_id_list):
        for i in range(len(poi_id_list)):
            poi_id_list[i] = str(poi_id_list[i])
        claim_dict = {
            "is_claimed": 1
        }
        NewShop.query.filter(NewShop.poi_id.in_(poi_id_list)).update(claim_dict)
        return 0

    @classmethod
    def update_owner_id(cls, mobile, user_id):
        update_dict = {
            "user_id": user_id
        }
        NewShop.query.filter(NewShop.mobile == mobile).update(update_dict)
        return 0

# _*_ coding: utf-8 _*_

from math import radians, cos, sin, asin, sqrt
from app.libs.poi_search.es_search_category import search
from app.libs.poi_search.es_search_street import search as search_street
from app.models.new_shop import NewShop as Shop
from app.models.group import Group
from app.models.new_user import NewUser as User
from app.model_views.shop import ShopCollection
from sqlalchemy import and_


class Recall:
    @staticmethod
    def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # 将十进制度数转化为弧度
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine公式
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # 地球平均半径，单位为公里
        return c * r * 1000

    @staticmethod
    def list_page(input_list, page, page_size):
        if page_size*page >= len(input_list):
            return input_list[(page-1)*page_size:]
        else:
            return input_list[(page-1)*page_size:page*page_size-1]

    def sort_by_distance(self, page, page_size, search_words, location, user_id, category=""):
        from time import time
        t1 = time()
        current_lat = float(location["lat"])
        current_lon = float(location["lon"])
        search_res = search(location, keyword=search_words, category=category)
        # print(search_res)
        #search_res = search(location, keyword=[search_words])
        search_res = self.list_page(search_res, page, page_size)
        if not search_res:
            res = {
                "total": 0,
                "current_page": page,
                "items": [],
            }
            return res

        t2 = time()
        print(t2-t1)
        filter_list = []
        for item in search_res:
            filter_list.append(item['_source']['id'])

        # shop_data_list = Shop.query.filter(Shop.poi_id.in_(filter_list)).paginate(page=page, per_page=page_size, error_out=False)
        shop_data_list = Shop.query.filter(Shop.poi_id.in_(filter_list)).all()
        group_data_list = Group.query.filter(and_(Group.user_openid == user_id, Group.status == 2)).all()
        group_data_dict = {}
        for group_data in group_data_list:
            group_data_dict[group_data.poi_id] = 1
        #print(shop_data_list.items)
        t3 = time()
        print(t3-t2)
        distance_list = []
        street_info_list = []
        for shop_data in shop_data_list:
            shop_lat = float(shop_data.latitude)/1e6
            shop_lon = float(shop_data.longitude)/1e6
            search_res_street = search_street({"lat": shop_lat, "lon": shop_lon}, keyword=[""])
            if len(search_res_street) <= 0:
                street_name = shop_data.district
            else:
                street_name = search_res_street[0]['_source']['name']
            street_info_list.append(street_name)
            distance = self.haversine(current_lon, current_lat, shop_lon, shop_lat)
            print(distance)
            distance_list.append(distance)
        t4 = time()
        print(t4-t3)

        shop_collection = ShopCollection(is_debug=True)
        shop_collection.fill(shop_data_list, distance_list, group_data_dict, street_info_list, user_id)
        #print(shop_collection.items)
        #print(shop_collection.items[0].name)

        res = {
            "total": 20,
            "current_page": page,
            "items": shop_collection.items,
        }
        return res













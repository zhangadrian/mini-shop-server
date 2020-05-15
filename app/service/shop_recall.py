# _*_ coding: utf-8 _*_

from math import radians, cos, sin, asin, sqrt
from app.libs.poi_search.es_search import search
from app.libs.poi_search.es_search_street import search as search_street
from app.models.shop import Shop
from app.models.group import Group
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

    def sort_by_distance(self, page, page_size, search_words, location, user_id):
        search_res = search(location, keyword=[search_words])
        #print(search_res)
        filter_list = []
        for item in search_res:
            filter_list.append(item['_source']['id'])

        shop_data_list = Shop.query.filter(Shop.poi_id.in_(filter_list)).paginate(page=page, per_page=page_size, error_out=False)
        group_data_list = Group.query.filter(and_(Group.user_openid == user_id, Group.status == 2)).all()
        group_data_dict = {}
        for group_data in group_data_list:
            group_data_dict[group_data.poi_id] = 1
        #print(shop_data_list.items)
        distance_list = []
        street_info_list = []
        current_lat = location["lat"]
        current_lon = location["lon"]
        for shop_data in shop_data_list.items:
            shop_lat = float(shop_data.latitude)/1e6
            shop_lon = float(shop_data.longitude)/1e6
            search_res_street = search_street({"lat": shop_lat, "lon": shop_lon}, keyword=[""])
            street_name = search_res_street[0]['_source']['name']
            street_info_list.append(street_name)
            distance = self.haversine(current_lon, current_lat, shop_lon, shop_lat)
            distance_list.append(distance)

        if page == 1:
            test_shop_data = Shop.query.filter(Shop.poi_id == "warrenyang_shop").first()
            shop_data_list.items.insert(0, test_shop_data)
            distance_list.insert(0, 10)
            test_shop_data = Shop.query.filter(Shop.poi_id == "haolin_shop").first()
            shop_data_list.items.insert(0, test_shop_data)
            distance_list.insert(0, 10)
        shop_collection = ShopCollection()
        shop_collection.fill(shop_data_list, distance_list, group_data_dict, street_info_list)
        #print(shop_collection.items)
        #print(shop_collection.items[0].name)

        res = {
            "total": shop_data_list.total,
            "current_page": shop_data_list.page,
            "items": shop_collection.items,
        }
        return res

    def get_shop_list(self, user_id, shop_id_list):
        group_data_list = Group.query.filter(and_(Group.user_openid == user_id, Group.status == 2)).all()
        group_data_dict = {}
        for group_data in group_data_list:
            group_data_dict[group_data.poi_id] = 1

        res_dict = {}
        for shop_id in shop_id_list:
            if shop_id in group_data_dict:
                res_dict[shop_id] = 1
        return res_dict



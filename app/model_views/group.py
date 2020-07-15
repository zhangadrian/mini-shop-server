# _*_ coding: utf-8 _*_
from app.model_views.base import ModelView
__author__ = "adhcczhang"


class BaseGroupView(ModelView):
    def __init__(self, group):
        self.group_name = group.group_name
        self.user_nickname = group.user_nickname
        self.shop_owner_nickname = group.shop_owner_nickname
        self.group_id = group.group_id
        self.poi_id = group.poi_id


class GroupCollection:
    def __init__(self):
        self.items = []

    def fill(self, group_list):
        self.items = [BaseGroupView(group_item) for group_item in group_list]
        return self.items



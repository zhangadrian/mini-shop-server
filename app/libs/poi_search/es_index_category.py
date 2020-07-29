# coding: utf-8

# 创建、删除索引

import os
import sys
import codecs
import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch([{'host':'127.0.0.1', 'port': 9200}])

INDEX_NAME = "index_category"
DIR_PATH = '/root/adhcczhang/aux/new_shops'


def delete_specific_index(index, index_id):
    body = {
        "query":{
            "term":{
                "id": index_id
            }
        }
    }
    result = es.delete_by_query(index=index, body=body)
    return result

def update_specific_index(index, index_id, update_dict):
    body = {
        "query": {
            "term": {
                "id": index_id
            }
        },
        "script": {
            "inline": "ctx._source.name = params.name",
            "params": update_dict,
        }
    }
    result = es.update_by_query(index=index, body=body)
    print(result)
    return result


def create_index(index):
    '''创建索引'''
    body = {
        "mappings" : {
            "poi" : {
                "properties" : {
                    "id" : {
                        "type" : "keyword",
                    },
                    "name" : {
                        "type" : "text",
                        "analyzer": "ik_max_word",  # ik_smart, ik_max_word
                        "search_analyzer": "ik_smart",
                    },
                    "address" : {
                        "type" : "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_smart",
                    },
                    "category": {
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_smart",
                    },
                    "mobile" : {
                        "type" : "keyword",
                    },
                    "location" : {
                        "type" : "geo_point",   # lon:[-180, 180], lat:[-90, 90]
                        #"geohash_prefix": true,
                        #"geohash_precision": "1km"
                    },
                }
            }
        }
    }

    if not es.indices.exists(index=index):
        result = es.indices.create(index=index, body=body)
        print(result)
    else:
        print('index allready exist: %s' % index)


def delete_index(index):
    '''删除索引'''
    #delete_by_all = {"query":{"match_all":{}}}
    #result = es.delete_by_query(index=index, body=delete_by_all)
    #print(result)
    if es.indices.exists(index=index):
        result = es.indices.delete(index=index)
        print(result)
    else:
        print('index not exist: %s' % index)

def change_category_old(category):
    category_list = category.split(":")
    if category_list[0] == "购物":
        if len(category_list) >=2:
            if category_list[1] == "便利店" or category_list[1] == "超市":
                return "购物"
    if category_list[0] == "美食":
        return "美食"
    if category_list[0] == "酒店宾馆":
        return "住宿"
    if category_list[0] == "汽车" or category_list[0] == "生活服务" or category_list[0] == "娱乐休闲":
        return "服务"
    if category_list[0] == "运动健身":
        return "健身"
    return "其他"

def change_category(category):
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


def insert_data(index, dir_path):
    '''插入数据'''
    import json
    for fn in os.listdir(dir_path):
        print(fn)
        f_path = os.path.join(dir_path, fn)
        actions = []
        start = time.time()
        for i, line in enumerate(codecs.open(f_path, 'r', encoding='utf-8')):
            try:
                eles = json.loads(line.strip())
                longitude = float(eles["longitude"])/1000000
                latitude = float(eles["latitude"])/1000000
                if abs(longitude) > 180 or abs(latitude) > 90:
                    #print('%d location error: %f %f' % (i, longitude, latitude))
                    continue
                #es.index(index=index, doc_type=INDEX_NAME, body={})
                category = change_category(eles["category"])
                action = {
                    '_op_type': 'index',
                    '_index': index,
                    '_type': 'poi',
                    '_source':{
                        'id': eles["id"],
                        'name': eles["name"],
                        'address': eles["address"],
                        'mobile': eles["phone"],
                        'category': category,
                        'location': {
                            'lon': longitude, 
                            'lat': latitude,
                        }
                    }
                }
                actions.append(action)
                if (i+1) % 100000 == 0: # bulk size 10~15M
                    helpers.bulk(client=es, actions=actions)
                    print('%d time cost %.2fs' % (i+1, time.time() - start))
                    actions = []
                    start = time.time()
            except Exception as e:
                print(e)
                continue 
        if len(actions) > 0:      
            helpers.bulk(client=es, actions=actions)
            print('%d time cost %.2fs' % (i+1, time.time() - start))
        print('--------------------------')


def main():
    if sys.argv[1] == 'create':
        create_index(INDEX_NAME)
    elif sys.argv[1] == 'delete':
        delete_index(INDEX_NAME)
    elif sys.argv[1] == 'insert':
        insert_data(INDEX_NAME, DIR_PATH)
    elif sys.argv[1] == "delete_specific_index":
        index_id = sys.argv[2]
        delete_specific_index(INDEX_NAME, index_id)
    elif sys.argv[1] == "update_specific_index":
        index_id = "xiaoxue_shop"
        update_dict = {
            "name": "这就是一个测试店名"
        }
        update_specific_index(INDEX_NAME, index_id, update_dict)


if __name__ == "__main__":
    main()

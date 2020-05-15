# coding: utf-8

# 创建、删除索引

import os
import sys
import codecs
import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch([{'host':'127.0.0.1', 'port': 9200}])

INDEX_NAME = "index_street_info"
DIR_PATH = './search_street'

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
                    "normalisedname" : {
                        "type" : "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_smart",
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


def insert_data(index, dir_path):
    '''插入数据'''
    for fn in os.listdir(dir_path):
        print(fn)
        f_path = os.path.join(dir_path, fn)
        actions = []
        start = time.time()
        for i, line in enumerate(codecs.open(f_path, 'r', encoding='utf-8')):
            try:
                eles = line.strip().split('\t')
                print(len(eles))
                if len(eles) != 15:
                    continue
                longitude = float(eles[5])
                latitude = float(eles[6])
                print(longitude)
                print(latitude)
                if abs(longitude) > 180 or abs(latitude) > 90:
                    #print('%d location error: %f %f' % (i, longitude, latitude))
                    continue
                #es.index(index=index, doc_type=INDEX_NAME, body={})
                action = {
                    '_op_type': 'index',
                    '_index': index,
                    '_type': 'poi',
                    '_source':{
                        'id': eles[0],
                        'name': eles[3],
                        'normalisedname': eles[4],
                        'location': {
                            'lon': longitude, 
                            'lat': latitude,
                        }
                    }
                }
                print(action)
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


if __name__ == "__main__":
    main()

# coding: utf-8

# 搜索

import os
import sys
import codecs
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host':'127.0.0.1', 'port': 9200}])

INDEX_NAME = "index_only_distance"


def query_all():
    """Queries all matches in Elasticsearch, to be used further for suggesting 
        product names when a user is not aware of them.
    """
    query_all = {
        "query": {"match_all": {}},
    }
    return query_all


def search_keyword(index, keywords, location,size=20, distance="5km"):
    result = es.search(index=index, doc_type='poi', body={
        'query': {
            'bool': {
                'should': [
                    {'match':{'name': keywords}}, 
                    {'match':{'address': keywords}}
                    ],
                'filter': {
                    "geo_distance": {
                        "distance": distance,
                        "location": {
                            "lat": float(location["lat"]),
                            "lon": float(location["lon"]),
                        }
                    }

                }
            }
        },
        "highlight": {
            "fields" : {
                "name" : {},
                "address": {},
            }
        },
        'from': 0,
        'size': size,
    })

    #for item in result['hits']['hits']:
    #    print(item)
    return result['hits']['hits']


def search_geometry(index, location, size=20, distance="10000km"):
    result = es.search(index=index, doc_type='poi', body={
        "query": {
            "bool": {
                "must" : {
                    "match_all" : {}
                },
                "filter": { 
                    "geo_distance": {
                        "distance": distance,
                        "location": {
                            "lat": float(location["lat"]),
                            "lon": float(location["lon"]),
                        }
                    }
                }
            }
        },
        'size': size,
    })

    #for item in result['hits']['hits']:
    #    print(item)
    return result['hits']['hits']

def search(location, keyword=[]):
    print(location)
    print(keyword)
    if keyword:
        keywords = ' '.join(keyword)
        search_res = search_keyword(INDEX_NAME, keywords, location)
    else:
        search_res = search_geometry(INDEX_NAME, location)
    return search_res

def main():
    if sys.argv[1] == 'key':
        keywords = ' '.join(sys.argv[2:])
        location = {
            'lat': 11.57,
            'lon': 2.68
        }
        search_keyword(INDEX_NAME, keywords, location)
    elif sys.argv[1] == 'geo':
        print(sys.argv[2])
        print(sys.argv[3])
        location = {'lon': float(sys.argv[2]), 'lat': float(sys.argv[3])}
        search_geometry(INDEX_NAME, location)



if __name__ == "__main__":
    main()

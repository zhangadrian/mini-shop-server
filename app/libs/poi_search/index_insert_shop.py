# coding: utf-8

import sys
import json

key_list = ["id", "name", "address", "category", "phone", "latitude", "longitude"]
output_list = []
for line in sys.stdin:
    line = line.strip()
    line_list = line.split()
    shop_info_dict = {}

    for item in list(zip(key_list, line_list)):
        shop_info_dict[item[0]] = item[1]

    json_str = json.dumps(shop_info_dict)
    print(json_str)




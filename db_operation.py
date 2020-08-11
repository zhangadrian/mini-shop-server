# _*_ coding = utf-8 _*_

import MySQLdb
import sys
import time
db_ip = '127.0.0.1'
db_port = '3306'
db_name = 'zerd'
db_user = 'root'
db_pass = 'root'


def update_shop_owner(poi_id_list, user_id_list):
    db = MySQLdb.connect(host=db_ip, port=int(db_port), db=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    vals = list(zip(poi_id_list, user_id_list))
    sql = "update shop_info set user_id= %s where poi_id= %s"
    cursor.executemany(sql, vals)
    db.commit()


if __name__ == "__main__":
    poi_id_list = ["bowen_shop"]
    user_id_list = ["ostTs4icZrBJuWTAFKm9nejcPrI8"]
    update_shop_owner(poi_id_list, user_id_list)


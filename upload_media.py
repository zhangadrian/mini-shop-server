# _*_ coding: utf-8 _*_

import subprocess
import requests

APP_ID = 'wxafc8a1a131f0eb7d'
APP_SECRET = '0b163686815e14682e43228ec19ce557'
get_access_token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}"
upload_media_url = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token={0}&type=image"

media_file_path = "./contact_me_qr.png"


def callback_access_token():
    get_url = get_access_token_url.format(APP_ID, APP_SECRET)
    res = requests.get(get_url)
    access_token = res.json()["access_token"]
    return access_token


def upload_media():
    import json

    access_token = callback_access_token()
    upload_url = upload_media_url.format(access_token)
    # cmd = "curl -F media=@contact_me_qr.png " + '"' + upload_url + '"'
    cmd = "curl -F media=@/root/adhcczhang/mini-shop-server/app/static/contact_me_qr.png " + upload_url
    print(cmd)

    process = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.stdout.decode('utf8')
    print(output)
    media_id = json.loads(output)["media_id"]

    return media_id


if __name__ == "__main__":
    import pickle

    res_file_path = "/root/adhcczhang/mini-shop-server/app/static/media_id.pkl"
    media_id = upload_media()
    res_dict = {
        "media_id": media_id
    }

    with open(res_file_path, 'wb') as res_file:
        pickle.dump(res_dict, res_file)

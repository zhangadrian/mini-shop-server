# _*_ coding: utf-8 _*_

from flask import current_app
import json
import os

from sts.sts import Sts

class TencentCos:
    def __init__(self):
        self.cos_secret_id = current_app.config["COS_SECRET_ID"]
        self.cos_secret_key = current_app.config["COS_SECRET_KEY"]

    def construct_config(self):
        config = {
            # 临时密钥有效时长，单位是秒
            'duration_seconds': 1800,
            'secret_id': self.cos_secret_id,
            # 固定密钥
            'secret_key': self.cos_secret_key,
            # 设置网络代理
            # 'proxy': {
            #     'http': 'xx',
            #     'https': 'xx'
            # },
            # 换成你的 bucket
            'bucket': '231n-1258195682',
            # 换成 bucket 所在地区
            'region': 'ap-nanjing',
            # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
            # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
            'allow_prefix': '*',
            # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
            'allow_actions': [
                # 简单上传
                'name/cos:PutObject',
                'name/cos:PostObject',
                # 分片上传
                'name/cos:InitiateMultipartUpload',
                'name/cos:ListMultipartUploads',
                'name/cos:ListParts',
                'name/cos:UploadPart',
                'name/cos:CompleteMultipartUpload'
            ],

        }

        return config

    def get_credential(self):
        config = self.construct_config()
        sts = Sts(config)
        response = sts.get_credential()
        return json.dumps(dict(response), indent=4)



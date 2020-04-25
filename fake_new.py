# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2018/5/12.
"""
from app import create_app

__author__ = 'Allen7D'
from app.models.base import db
from app.models.new_user import NewUser

app = create_app()
with app.app_context():
    with db.auto_commit():
        # 创建一个超级管理员
        user = NewUser()
        user.openid = '999'
        user.nickname = 'Super'
        db.session.add(user)

    with db.auto_commit():
        # 创建一个普通管理员
        user = NewUser()
        user.openid = '777'
        user.nickname = 'Admin'
        db.session.add(user)

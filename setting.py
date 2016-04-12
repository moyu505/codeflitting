# -*- coding: UTF-8 -*-
import os

#Mysql 配置
if 'SERVER_SOFTWARE' in os.environ:
    MYSQL_DB = 'ypPyUecKCCCkBZcVqCCT'  ##bae数据库名称
    MYSQL_USER = 'qRWe3tSO79Y5v8OSVgvAKlIF'
    MYSQL_PASS = '8q0vQg9W8NVRTgpQ2KKrGkIbyf8KC46u'
    MYSQL_HOST = 'sqld.duapp.com:4050'
else :
    MYSQL_DB = 'pycoder'  ##本地数据库名称
    MYSQL_USER = 'root'
    MYSQL_PASS = ''
    MYSQL_HOST = '127.0.0.1:3306'


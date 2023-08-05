#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time    : 2019/5/1 23:26
# @Email  : jtyoui@qq.com
# @Software: PyCharm
from platform import platform
import os
import bz2
import json
import re

re_id_card = """
(?P<province>[^省]+省|.+自治区)
(?P<city>[^自治州]+自治州|[^市]+市|[^盟]+盟|[^地区]+地区|.+区划)
(?P<county>[^市]+市|[^县]+县|[^旗]+旗|[^区]+区)?
(?P<town>[^区]+区|[^镇]+镇)?
(?P<village>.*)
""".replace('\n', '')

_Address = {}


def _load(file_address):  # 下载地址的压缩包
    from urllib.request import urlretrieve
    url = 'https://dev.tencent.com/u/zhangwei0530/p/logo/git/raw/master/rear.bz2'
    place = urlretrieve(url, file_address)  # 下载
    print('---------验证数据-------')
    if not os.path.exists(file_address):
        print('下载失败')
    elif os.stat(file_address).st_size != 2292518:
        print('下载失败、移除无效文件！')
        os.remove(file_address)

    print('\033[1;33m' + place[0])


def find_address(name):
    """查询地址。输入一个地名，查到这个名字的详细地址：比如输入：大连市、朝阳区、遵义县、卡比村等
    :param name: 输入一个地址。
    :return: 地址的信息
    """
    assert True if name else False, '输入的字符串不能为空'
    global _Address
    if not _Address:
        if 'Windows' in platform():
            path = r'D:/jtyoui_address'
        else:
            path = r'./jtyoui_address'
        if not os.path.exists(path):
            _load(path)
        bz = bz2.BZ2File(path)
        text = bz.read().decode('utf-8')
        data = text[512:-1134]
        _Address = json.loads(data, encoding='utf8')
    address = []
    for province in _Address:
        city_s = _Address[province]
        for city in city_s:
            districts = city_s[city]
            for district in districts:
                towns = districts[district]
                for town in towns:
                    villages = towns[town]
                    for village in villages:
                        if name in village:
                            addr = province + ' ' + city + ' ' + district + ' ' + town + ' ' + village
                            address.append(addr)
                    if name in town:
                        addr = province + ' ' + city + ' ' + district + ' ' + town
                        address.append(addr)
                if name in district:
                    addr = province + ' ' + city + ' ' + district
                    address.append(addr)
            if name in city:
                addr = province + ' ' + city
                address.append(addr)
        if name in province:
            addr = province
            address.append(addr)
    return address


def find_identity_card_address(card_addr):
    names = re.match(re_id_card, card_addr)
    province = names.group('province')
    city = names.group('city')
    county = names.group('county')
    town = names.group('town')
    village = names.group('village')
    return province, city, county, town, village


if __name__ == '__main__':
    import pprint

    pprint.pprint(find_address('晋安'))
    print(find_identity_card_address('贵州省贵阳市南明区花果园延安南路28号'))

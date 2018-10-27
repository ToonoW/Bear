import json
import logging

import requests_html
from faker import Faker

logger = logging.getLogger('honey')
faker = Faker()
session = requests_html.HTMLSession()


def _honeycomb_create(name, email, password, **kwargs):
    data = {
        'name': name,
        'email': email,
        'passwd': password,
        'repasswd': password,
        'wechat': kwargs['qq'],
        'imtype': 2,
        'code': 0,
    }
    r = session.post('https://susanoocloud.com/auth/register', data=data)
    try:
        if not '注册成功' in json.loads(r.text)['msg']:
            return None
        return (name, email, password)
    except Exception as e:
        logger.error('Registe failure.', e)
        return None


def honeycomb_create():
    info = _honeycomb_create(faker.name(), faker.email(), faker.password(), qq=faker.random_number())
    return info


def _honeycomb_login(email, password):
    data = {
        'email': email,
        'passwd': password,
    }
    r = session.post('https://susanoocloud.com/auth/login', data=data)
    if r.url != 'https://susanoocloud.com/user':
        try:
            if '登录成功' not in json.loads(r.text)['msg']:
                return None
        except Exception as e:
            logger.error('Login failure.', e)
            return None
    return (email, password)


def honeycomb_login(email, password):
    return _honeycomb_login(email, password)


def _honeycomb_info():
    is_checkin = False
    r = session.get('https://susanoocloud.com/user')
    if 'login' in r.url:
        raise Exception('Login required.')
    if r.html.search('今日已签到') is not None:
        is_checkin = True
    remaining_count = r.html.search('剩余可用 {}% {}GB')[1]
    return (remaining_count, is_checkin)


def honeycomb_info(email, password):
    if _honeycomb_login(email, password) is None:
        raise Exception('Login required.')
    return _honeycomb_info()


def _honey_info():
    r = session.get('https://susanoocloud.com/user/node')
    if 'login' in r.url:
        raise Exception('Login required.')
    nodes = [node.xpath('//font/text()') for node in
             r.html.xpath('//div[@class="col-lg-12 col-sm-12"][1]//div[@class="text-overflow"]')]
    nodes_ids = [int(url[11:-6]) for url in
                 r.html.xpath('//div[@class="col-lg-12 col-sm-12"][1]//p[@class="card-heading"]/a/@onclick')]
    nodes_json = []
    for ids in nodes_ids:
        url = 'https://susanoocloud.com/user/node/{}?ismu=0&relay_rule=0'.format(ids)
        r_node = session.get(url)
        nodes_json.append(json.loads(r_node.html.xpath('//div[@id="ssr_json"]/textarea/text()', first=True)))

    configs = []
    for node_infos, node_config in zip(nodes, nodes_json):
        name = node_infos[0]
        load = int(node_infos[2][3:-1])
        node_config['name'], node_config['load'] = name, load
        configs.append(node_config)
    return configs


def honey_info(email, password):
    if _honeycomb_login(email, password) is None:
        raise Exception('Login required.')
    return _honey_info()
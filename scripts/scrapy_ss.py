import json

from faker import Faker
import requests_html


faker = Faker()
email = faker.email()
name = faker.name()
passwd = faker.password()
qq = faker.random_number()

session = requests_html.HTMLSession()

r_register = session.post('https://susanoocloud.com/auth/register', data={
    'email': email,
    'name': name,
    'passwd': passwd,
    'repasswd': passwd,
    'wechat': qq,
    'imtype': 2,
    'code': 0,
})
if r_register.status_code != 200:
    raise Exception('注册失败')
print('注册成功')
print('email: {} , passwd: {}'.format(email, passwd))

r_login = session.post('https://susanoocloud.com/auth/login', data={
    'email': email,
    'passwd': passwd,
})
if r_login.status_code != 200:
    raise Exception('登陆失败')
print('登陆成功')

r_user = session.get('https://susanoocloud.com/user')
if r_user.status_code != 200:
    raise Exception('获取用户信息失败')
print('获取用户信息成功')

if r_user.html.search('今日已签到') is not None:
    print('已经签到过了')
else:
    r_checkin = session.post('https://susanoocloud.com/user/checkin')
    if r_checkin.status_code == 200:
        print('签到成功')

result = r_user.html.search('剩余可用 {}% {}GB')
print('剩余流量 {}% {}GB'.format(result[0], result[1]))

r_nodes = session.get('https://susanoocloud.com/user/node')
nodes = [node.xpath('//font/text()') for node in
         r_nodes.html.xpath('//div[@class="col-lg-12 col-sm-12"][1]//div[@class="text-overflow"]')]
nodes_ids = [int(url[11:-6]) for url in
             r_nodes.html.xpath('//div[@class="col-lg-12 col-sm-12"][1]//p[@class="card-heading"]/a/@onclick')]
print(nodes)
print(nodes_ids)

nodes_json = []
for ids in nodes_ids:
    url = 'https://susanoocloud.com/user/node/{}?ismu=0&relay_rule=0'.format(ids)
    r_node = session.get(url)
    nodes_json.append(json.loads(r_node.html.xpath('//div[@id="ssr_json"]/textarea/text()', first=True)))

print(nodes_json)
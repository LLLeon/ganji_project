from bs4 import BeautifulSoup
import requests
import pymongo
import random


# 创建数据库
client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
url_list = ganji['url_list']
item_info = ganji['item_info']

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
    'Cookie': 'ganji_xuuid=48cc5855-ca7c-445b-93fe-ac1f3c2bf72d.1458825236270; ganji_uuid=3682637680349351514952; citydomain=bj; GANJISESSID=e9556aac34e86b3c2b939f2c5a63e7dd; statistics_clientid=me; hotPriceTip=1; STA_DS=1; _gl_tracker=%7B%22ca_source%22%3A%22study.163.com%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22other_study.163.com%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A48595868035%7D',
    'Connection': 'keep-alive'
}
proxy_list = [
    'http://115.148.70.109',
    'http://115.223.224.73',
    'http://218.20.241.28',
    'http://113.78.29.36'
]
proxy_ip = random.choice(proxy_list)
proxies = {'http':proxy_ip}


# 获取商品链接
def get_links_from(channel, pages, who_sells='1'):
    list_view = '{}a{}o{}/'.format(channel, str(who_sells), str(pages))
    wb_data = requests.get(list_view, headers=headers, proxies=proxies)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    # 检测该页面是否有商品
    if soup.find('ul', 'pageLink clearfix'):  # 此标签为页面底部页码的标签
        links = soup.select('dd.feature > div > ul > li > a')
        for link in links:
            item_link = link.get('href')

            # 判断数据库中是否已有此条链接
            if url_list.find_one({'url': item_link}):
                print('老大,已经抓过这条链接啦~')
            else:
                url_list.insert_one({'url': item_link})
                print('老大,新链接抓到啦:', item_link)
    else:
        print('老大,{}类别的二手货链接已经抓完啦~'.format(str(channel.split('/')[-2])))


# get_links_from('http://bj.ganji.com/shouji/', 1000)


# 抓取商品详情
def get_item_info(url):
    wb_data = requests.get(url, headers=headers)
    try:

    # 测试该页面商品是否还存在
        if wb_data.status_code == 404:
            print('老大,二手货被人买走啦~')
        else:
            soup = BeautifulSoup(wb_data.text, 'lxml')
            title = soup.select('h1.title-name')[0]
            date = list(soup.select('i.pr-5')[0].stripped_strings)[0]
            type = soup.select('div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(1) > span > a:nth-of-type(1)')[0]
            price = soup.select('i.f22.fc-orange.f-type')[0]
            area = list(map(lambda x: x.text, soup.select('ul.det-infor > li:nth-of-type(3) > a')))
            data = {
                'title': title.get_text(),
                'date': date.replace(u'\xa0', ''),  # 去除 '\xa0'
                'type': type.get_text(),
                'price': price.get_text(),
                'area': area[1:],
                'url': url
            }

            # 检测数据库中是否已抓取此条信息
            if item_info.find_one({'url': url}):
                print('老大,这个二手货的信息咱们已经抓过啦~')
            else:
                item_info.insert_one(data)
                print('老大,新鲜的信息来啦~')
    except IndexError:
        pass



# for item in url_list.find():
#     get_item_info(item['url'])
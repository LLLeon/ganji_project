from multiprocessing import Pool
from channel_extract import channel_list
from page_parsing import get_links_from, get_item_info, url_list


# 抓取所有类型二手物品的链接
def get_all_link_from(channel):
    for page in range(1, 101):
        get_links_from(channel, page)


if __name__ == '__main__':
    pool = Pool()
    # pool.map(get_all_link_from, channel_list.split())
    pool.map(get_item_info, [urls['url'] for urls in url_list.find()])

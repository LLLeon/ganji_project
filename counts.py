import time
from page_parsing import url_list, item_info


while True:
    print('url_list:', url_list.find().count())
    time.sleep(5)
    print('item_info:', item_info.find().count())
    time.sleep(5)
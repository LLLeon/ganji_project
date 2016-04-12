
# coding: utf-8

# In[1]:

import pymongo
import charts


# In[2]:

client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
item_info = ganji['sample_3']


# In[20]:

# 定制管道，查找一天内交易的商品所在城区及分别交易数量
pipeline = [
    {'$match':  {'time': 1}},
    {'$group': {'_id': {'$slice': ['$area', 0, 1]}, 'counts': {'$sum': 1}}},
    {'$sort': {'counts': -1}}
     ]


# In[21]:

for i in item_info.aggregate(pipeline):
    print(i)


# In[22]:

def data_gen(time):
    pipeline = [
    {'$match':  {'time': time}},
    {'$group': {'_id': {'$slice': ['$area', 0, 1]}, 'counts': {'$sum': 1}}},
    {'$sort': {'counts': -1}}
     ]
    for i in item_info.aggregate(pipeline):
        yield [i['_id'][0], i['counts']]


# In[23]:

for i in data_gen(1):
    print(i)


# In[24]:

series = [{
        'type': 'pie',
        'name': 'pie chart',
        'data': [i for i in data_gen(1)]
    }]
options = {
    'chart': {'zoomType': 'xy'},
    'title': {'text': '发帖量统计'},
    'subtitle': {'text': '一天内交易成功的二手商品，各城区交易量饼图'}
}
charts.plot(series, options = options, show = 'inline')


# In[ ]:




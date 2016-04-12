
# coding: utf-8

# In[2]:

from pymongo import MongoClient
import charts


# In[4]:

client = MongoClient('localhost', 27017)
ganji = client['ganji']
item_info = ganji['sample_3']


# In[29]:

# 创建管道，以层层筛选元素，此条管道最终是筛选出：12月24日发布，且第4天售出的商品，出现次数最多的三个价格
pipeline = [
    {'$match': {'$and': [{'pub_date': '2015.12.24'}, {'time': 3}]}},  # 匹配24日发布且第4天售出的商品
    {'$group': {'_id': '$price', 'counts': {'$sum': 1}}},  # 以price为'_id'的值来分组，counts为此price出现的次数，sum值为每次加几
    {'$sort': {'counts': -1}},  # counts值为1时是从小到大排序，为-1时则反之
    {'$limit': 3}
]
# 'pub_date': '2015.12.24'


# In[30]:

for i in item_info.aggregate(pipeline):
       print(i)


# In[36]:

pipeline2 = [
    {'$match': {'$and': [{'pub_date': '2015.12.25'}, {'time': 1}]}},
    {'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},  # 以_id分组，取cate元素中跳过2个选1个（第3个）
    {'$sort': {'counts': -1}}
]


# In[37]:

for i in item_info.aggregate(pipeline2):
    print(i)


# In[48]:

# 定义为函数
def data_gen(date, time):
    pipeline = [
    {'$match': {'$and': [{'pub_date': date}, {'time': time}]}},
    {'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},
    {'$sort': {'counts': -1}}
]
    for i in item_info.aggregate(pipeline):
        yield [i['_id'][0], i['counts']]


# In[49]:

for i in data_gen('2016.01.10', 1):
    print(i)


# In[53]:

series = [{
        'type': 'pie',
        'name': 'pie chart',
        'data': [i for i in data_gen('2016.01.10', 1)]
    }]
options = {  # 可从highcharts官网查找
    'chart': {'zoomType': 'xy'},
    'title': {'text': '发帖量统计'},
    'subtitle': {'text': '2016.01.10二手物品在随后七天内，交易时长为1天的类目占比'}
}
charts.plot(series, options=options, show='inline')


# In[ ]:




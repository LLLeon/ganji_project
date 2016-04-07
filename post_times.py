
# coding: utf-8

# In[18]:

import pymongo
import charts


# In[11]:

client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
item_info = ganji['sample_copy']


# In[8]:

for i in item_info.find().limit(300): # 查看数据库
    print(i['cates'])


# In[12]:

for i in item_info.find():
    if len(i['cates']) >= 3:  # 如果此中元素大于等于3，判断取第三项
        cates = i['cates'][2]
    if i['cates'] == []:
        cates = '不明'
    item_info.update({'_id': i['_id']}, {'$set': {'cates': cates}})


# In[13]:

for i in item_info.find().limit(300):
    print(i['cates'])


# In[14]:

cates_list = []
for i in item_info.find():
    cates_list.append(i['cates'])
cates_index = list(set(cates_list))
print(cates_index)


# In[15]:

post_times = []  # 计算各类发帖次数
for index in cates_index:
    post_times.append(cates_list.count(index))
print(post_times)


# In[16]:

def data_gen(types):
    length = 0
    for cates, times in zip(cates_index, post_times):
        if length <= len(cates_index):
            data = {
                'name': cates,
                'data': [times],  # 切记把数量加入list中
                'type': types
            }
            yield data
            length += 1


# In[20]:

for i in data_gen('column'):
    print(i)


# In[22]:

series = [data for data in data_gen('column')]
charts.plot(series, show = 'inline', options = dict(title = dict(text = '北京各类别二手物品发帖量')))


# In[ ]:





# coding: utf-8

# In[46]:

from pymongo import MongoClient
from datetime import date, timedelta
import charts


# In[14]:

client = MongoClient('localhost', 27017)
ganji = client['ganji']
item_info = ganji['sample']


# In[20]:

for i in item_info.find({}, {'area': {'$slice': 1}, 'pub_date': 1, '_id': 0}).limit(300):  # 练习find用法
    print(i)


# In[21]:

for i in item_info.find({}, {'pub_date': 1, '_id': 0}).limit(300):  # 查看日期格式
    print(i)


# In[30]:

for i in item_info.find():  # 将日期统一格式为XXXX.XX.XX
    frags = list(i['pub_date'].split('-'))
    if len(frags) == 1:  # 如果格式为XXXX.XX.XX则未split，取第一个元素
        date = frags[0]
    else:
        date = '{}.{}.{}'.format(frags[0], frags[1], frags[2])
    item_info.update_one({'_id': i['_id']}, {'$set': {'pub_date': date}})


# In[42]:

def get_all_dates(date1, date2):  # 获取时间段内日期的函数，让程序能够明白这是日期
    the_date = date(int(date1.split('.')[0]), int(date1.split('.')[1]), int(date1.split('.')[2]))  # 注意使用int
    end_date = date(int(date2.split('.')[0]), int(date2.split('.')[1]), int(date2.split('.')[2]))
    days = timedelta(days=1)
    while the_date <= end_date:
        yield the_date.strftime('%Y.%m.%d')  # 生成起始阶段内的日期
        the_date += days  # 以一天为增长幅度循环


# In[50]:

def get_data_within(date1, date2, cates):  # 主函数
    for cate in cates:  # 类别循环
        cate_day_posts = []  # 单日某类别发帖量加入list中
        for date in get_all_dates(date1, date2):  # 单日某类别发帖量
            a = list(item_info.find({'pub_date': date, 'cates': cate}))  # 查找指定日期内指定类别的元素，放入list中
            each_day_posts = len(a)  # 某类别单日发帖量
            cate_day_posts.append(each_day_posts)
        data = {
            'name': cate,
            'data': cate_day_posts,
            'type': 'line'
        }
        yield data


# In[44]:

for i in get_data_within('2015.12.24', '2016.1.5', ['北京二手手机']):  # 测试函数
    print(i)


# In[51]:

options = {
    'chart': {'zoomType': 'xy'},
    'title': {'text': '发帖量统计'},
    'subtitle': {'text': '可视化统计图表'},
    'xAxis': {'categories': [i for i in get_all_dates('2015.12.24', '2016.1.5')]},
    'yAxis': {'title': {'text': '数量'}}
}
series = [i for i in get_data_within('2015.12.24', '2016.1.5', ['北京二手手机', '北京二手笔记本', '北京二手台式机/配件'])]
charts.plot(series, show='inline', options=options)


# In[ ]:




#  dayang-sdk-python  documents

dayang-sdk-python 是一个大洋的第三方 Python SDK, 实现了平台账号查询，事件跟踪，传播分析等 API。



## 安装

dayang-sdk-python 可以使用pip从pypi安装

```
pip install dayang-sdk-python
```

## 下载

dayang-sdk-python 在pypi上可用: https://pypi.org/project/dayang-sdk-python/

文档托管在:  https://github.com/wqfff/dayang-sdk-python/blob/master/README.md

## 代码

代码和问题跟踪托管在github上: https://github.com/wqfff/dayang-sdk-python



## 更新日志

Version 0.3(2019-09-26)

- 修复已知bug
- 更新README

Version 0.2(2019-09-26)

- 更新README

Version 0.1(2019-09-25)

- 发布

## 示例

### Client examples

Let’s begin our trip:

```python
>>>from dayangpy import Client
>>>client = Client(tenant_id, user_id, client_id, client_secret)
>>>client
<dayangpy.Client at 0x10fb8f6a0>
>>>client.access_token
'eyJ0eXAiOiJKV...DM2MzY4L'
```

<hr>

**Prepare the environment when you call the following example**

```
>>>from dayangpy import Client
>>>client = Client(tenant_id, user_id, client_id, client_secret)
```

### Platform examples

1. Search website account list

```python
>>>client.platform.get_website(like='人民网', page=1, page_size=3)
[{'level': 0,
  'site_id': '20190409191748082',
  'site_name': '人民网教育频道',
  'parent_id': '-1',
  'standard_tag': '/20190409191748082'},
 {'level': 0,
  'site_id': '20190409191900519',
  'site_name': '人民网四川频道滚动',
  'parent_id': '-1',
  'standard_tag': '/20190409191900519'},
 {'level': 0,
  'site_id': '20190326165954559',
  'site_name': '人民网本地站',
  'parent_id': '-1',
  'standard_tag': '/20190326165954559'}]
```



2. Search area list

```python
>>>client.platform.get_area(7362)
[{'area_id': '7363',
  'standard_tag': '/天津市',
  'show_name': '天津',
  'parent_area_id': '7362'}]
```



### News examples

1. Search news

```python
>>>client.news.search(title_like='中国')
[{'title': '<em>中国</em>生态文明建设大讲堂走进江西上饶宣讲会暨市委理论学习中心组集体学习（扩大）会举行',
  'summary': '点开图片快点行动就等你啦！中国生态文明建设大讲堂走进江西上饶宣讲会暨市委理论学习中心组集体学习（扩大）会举行',
  'resource_id': '6a690f51-9c2d-49bc-b8ff-830949c03c1b',
  'standard_publish_media_id': '2020180408185235530',
  'standard_publish_media_name': '上饶日报',
  'content_classify': ['环境'],
  'origin_url': 'http://mp.weixin.qq.com/s?__biz=MzA3NjEzNDYzNw==&mid=2651102850&idx=3&sn=673d74c839a8b303d0e441487807784d&scene=0',
  'create_time': '2019-09-26 15:30:42',
  'publish_time': '2019-09-26 15:28:21',
  'media_type': 2,
  'first_image_path': 'http://mmbiz.qpic.cn/mmbiz_jpg/oDqd7bkURtImru4dvMia7SdujQibdKZnanpNibMXoul6eQCzwFMic0h1j1k3p1zjfnotFHiagxcQRZZSqLA9jicaBobg/0?wx_fmt=jpeg',
  'standard_mention_region_tags': ['/江西省/上饶市'],
  'news_imgs': ['http://mmbiz.qpic.cn/mmbiz_jpg/oDqd7bkURtImru4dvMia7SdujQibdKZnanpNibMXoul6eQCzwFMic0h1j1k3p1zjfnotFHiagxcQRZZSqLA9jicaBobg/0?wx_fmt=jpeg'],
  'current_dynamic_data': {'comment_count': None,
   'transmit_count': None,
   'like_count': 1,
   'read_count': 3,
   'reward_count': None,
   'create_time': '2019-09-26 15:30:42'}},
 {'title': '中卫市举办文艺演出庆祝2019年<em>中国</em>农民丰收节',
  'summary': '9月24日，由市委宣传部、市旅游和文体广电局主办，市农业农村局承办的庆祝2019年中国农民丰收节广场文艺演出在市区文化广场举办。文艺演出在舞蹈的美妙舞姿中掌声。文艺演出在舞蹈中落下帷幕。',
  'resource_id': '4d390e95-0f40-4457-bda4-b938eadbc822',
  'standard_publish_media_id': '20180124203155549',
  'standard_publish_media_name': '宁夏电视台',
  'content_classify': ['时政'],
  'origin_url': 'http://news.nxtv.com.cn/nxnews/zwnews/2019-09-26/491202.html',
  'create_time': '2019-09-26 15:29:43',
  'publish_time': '2019-09-26 15:24:15',
  'media_type': 0,
  'first_image_path': '',
  'standard_mention_region_tags': ['/宁夏回族自治区/中卫市'],
  'current_dynamic_data': {'comment_count': None,
   'transmit_count': None,
   'like_count': None,
   'read_count': None,
   'reward_count': None,
   'create_time': None}}
]
```



2. Search news detail

```python
>>>client.news.get_detail('4d390e95-0f40-4457-bda4-b938eadbc822')  
{'title': '中卫市举办文艺演出庆祝2019年中国农民丰收节',
 'summary': '9月24日，由市委宣传部、市旅游和文体广电局主办，市农业农村局承办的庆祝2019年中国农民丰收节广场文艺演出在市区文化广场举办。文艺演出在舞蹈的美妙舞姿中拉声。文艺演出在舞蹈中落下帷幕。',
 'keywords': ['农业', '乡村', '舞蹈', '丰收节', '发展'],
 'author': '',
 'resource_id': '4d390e95-0f40-4457-bda4-b938eadbc822',
 'standard_publish_media_id': '20180124203155549',
 'standard_publish_media_name': '宁夏电视台',
 'content_classify': ['时政'],
 'origin_url': 'http://news.nxtv.com.cn/nxnews/zwnews/2019-09-26/491202.html',
 'create_time': '2019-09-26 15:29:43',
 'publish_time': '2019-09-26 15:24:15',
 'media_type': 0,
 'first_image_path': '',
 'standard_mention_region_tags': ['/宁夏回族自治区/中卫市'],
 'current_dynamic_data': {'comment_count': None,
  'transmit_count': None,
  'like_count': None,
  'read_count': None,
  'reward_count': None,
  'create_time': None},
 'content_raw': '<p>9月24日，由市委宣传部、市旅游和文体广电局主办，市农业农村局承办的庆祝2019年中国农民丰收节广场文艺演出在市区文化广场举办。</p> \n<p>文艺演出在乐快板《乡村振兴歌飞扬》、鼓板乐舞《欢庆丰收节》等12个精彩节目，吸引了众多市民驻足观看，并赢得阵阵掌声。文艺演出在舞蹈《在希望的田野上》中落下帷幕。</p> \n<p>据了、品牌强农和效益优先，按照“一带两廊”发展规划布局，对标全面建成小康社会硬任务，深入实施乡村振兴战略，进一步深化农业供给侧结构性改革，有序推进乡村振兴各项任务，农业农村经济发展呈现持续向好、稳中有进的良好势头。（见习记者 房媛 全媒体记者 何昱萱）</p>'}

```



### Tracker examples

1. create event tracker

```python
>>>client.tracker.create(1,'中华','中国') 
4338857
```

2. event tracker list

```python
>>>client.tracker.list()
[{'trackerId': '4338857',
  'trackerName': '中华',
  'mustContainWords': '中国',
  'trackerType': 1,
  'createTenantId': '235',
  'createUserId': '255',
  'createTime': '2019-09-26 15:39:21'},
```

3. get event tracker hotwords

```python
>>>client.tracker.get_hotwords(4338857)
[{'name_zh': '中国', 'count': '1425012.93', 'name_en': ''},
 {'name_zh': '新中国', 'count': '660874.80', 'name_en': ''},
 {'name_zh': '国家', 'count': '574817.81', 'name_en': ''},
 {'name_zh': '企业', 'count': '494464.78', 'name_en': ''},
 {'name_zh': '人民', 'count': '473758.54', 'name_en': ''},
	...
]
```

### Hotspot examples

1. get hotspot list

```python
>>>client.hotspot.list('poi','desc','1')
[{'eventId': '89a7801c-148b-4bc9-b4eb-b41c806084b9_d',
    'title': '王毅会见意大利外长迪马约',
    'summary': '新华社联合国9月25日电当地时间25日，国务委员兼外长王毅在纽约出席联合国大会期间会见意大利外长迪马约。王毅表示，今年3月，习近平主席对意大利进行成功国交往，巩固好政治互信，推动双边关系取得新的发展。双方要积极落实共建“一带一路”合作谅解备忘录，商定第三方市场合作重点项目，利用意大利作为主宾国参加第二届中国国际进口作，共同维护多边主义和自由贸易。希望意大利继续为推动中欧关系作出积极贡献。',
    'behalfImagePath': '',
    'currentHeat': 1559.6265726152765,
    'eventClassifyIds': ['1'],
    'eventClassifyNames': ['时政'],
    'standardPublishRegionTags': ['/湖南省'],
    'standardReferRegionTags': [],
    'createTime': '2019-09-26 14:19:36',
    'modifyTime': '2019-09-26 16:20:44',
    'originCreateTime': '2019-09-26 14:19:36',
    'favorite': False},
   {'eventId': 'efeb0441-5328-4a30-8bf1-e56bd47a8996_d',
    'title': '甘肃武威市委原书记火荣贵一审获刑18年',
    'summary': '新京报快讯据定西市中级人民法院官方微信消息，2019年9月26日，甘肃省定西市中级人民法院依法公开宣判甘肃省政协农业和农村工作委员会原副主任火荣贵受贿、三年;以滥用职权罪，判处有期徒刑五年，数罪并罚，决定执行有期徒刑十八年，并处罚金人民币100万元。',
    'behalfImagePath': '',
    'currentHeat': 1505.3684196083602,
    'eventClassifyIds': ['2'],
    'eventClassifyNames': ['社会'],
    'standardPublishRegionTags': ['/广东省/广州市'],
    'standardReferRegionTags': [],
    'createTime': '2019-09-26 15:11:52',
    'modifyTime': '2019-09-26 16:20:49',
    'originCreateTime': '2019-09-26 15:11:52',
    'favorite': False}
]

```



### Rank examples

1. get hotsearch list

```python
>>>client.rank.get_hotsearch('360_so', 'sports')
[{'title': '龚雪',
  'href': 'http://trends.so.com/result/trend?keywords=龚雪&time=30',
  'info': '13500',
  'indexNo': 1},
 {'title': '张常宁',
  'href': 'http://trends.so.com/result/trend?keywords=张常宁&time=30',
  'info': '10818',
  'indexNo': 2},
 .....
]

```

2. get wechat list

```python
 [{'billboardId': '107562_day_2019-08-30',
    'billboardTimeType': 'day',
    'billboardType': 0,
    'billboardTime': '2019-08-30',
    'nicknameId': '107562',
    'wxNickname': '人民日报',
    'wxName': 'rmrbwx',
    'wxBiz': 'MjM5MjAxNDM4MA==',
    'wxLogo': 'http://wx.qlogo.cn/mmhead/Q3auHgzwzM5Dlw4H8vWoicXPXccEVkWYgFE1pNUvX7uaHmafPODGIEA/132',
    'wxTypeName': '媒体',
    'urlTimes': 13,
    'urlNum': 24,
    'readnumAll': 2400024,
    'urlTimesReadnum': 1300013,
    'readnumAv': 100001.0,
    'likenumAll': 352655,
    'wci': 1777.24,
    'wciUp': 26.39,
    'standardRegionTag': '/北京市/北京市',
    'favorite': False},
   {'billboardId': '107562_month_2019-08-31',
    'billboardTimeType': 'month',
    'billboardType': 0,
    'billboardTime': '2019-08-31',
    'nicknameId': '107562',
    'wxNickname': '人民日报',
    'wxName': 'rmrbwx',
    'wxBiz': 'MjM5MjAxNDM4MA==',
    'wxLogo': 'http://wx.qlogo.cn/mmhead/Q3auHgzwzM5Dlw4H8vWoicXPXccEVkWYgFE1pNUvX7uaHmafPODGIEA/0',
    'wxTypeName': '媒体',
    'urlTimes': 390,
    'urlNum': 762,
    'readnumAll': 76200762,
    'urlTimesReadnum': 39000390,
    'readnumAv': 100001.0,
    'likenumAll': 9888478,
    'wci': 1775.3,
    'wciUp': 25.09,
    'standardRegionTag': '/北京市/北京市',
    'favorite': False}
    ....
   ]
```



### Spread examples

1. create spread

```python
>>>client.spread.create('5df607271a', '最美奋斗者海军372潜艇先进群体', '原标题：最美奋斗者 海军372潜艇先...')
[{
 "id": "6dd195df607271ac640d80faa516dfd4",
 "success": true,
 "taskId": "1e5d68df-9411-4da0-b511-df51edf80d34",
 "errorMsg": null
}]
```

2. get spread detail

```python
>>>client.spread.get_detail('1e5d68df-df51edf80d34')
[{'success': True,
  'errorMsg': None,
  'taskId': '1e5d68df-df51edf80d34',
  'taskStatus': 1,
  'taskResult': '分析完成有数据',
  'title': '最美奋斗者海军372潜艇先进群体',
  'count': 2,
  'list': [{'newsId': '246f6d2f-def1-441a-bab1-7afbb5bb394f',
    'newsTitle': '最美奋斗者 海军372潜艇先进群体',
    'newsUrl': 'http://news.cctv.com/2019/09/26/ARTI6JBHRDhJn9Q2OpfYufw8190926.shtml',
    'mediaName': '央视网',
    'publishTime': '2019-09-26 16:40:00',
    'reprintedCount': None,
    'commentCount': None,
    'likeCount': None,
    'readCount': None,
    'newsMediaType': 'web',
    'originAuthorName': '央视网',
    'emotion': 1},
   {'newsId': 'abd51fb9-2c97-407a-8096-81184ae71598',
    'newsTitle': '最美奋斗者 海军372潜艇先进群体',
    'newsUrl': 'http://www.sohu.com/a/343560671_428290#comment_area',
    'mediaName': '央视网',
    'publishTime': '2019-09-26 16:42:00',
    'reprintedCount': None,
    'commentCount': None,
    'likeCount': None,
    'readCount': None,
    'newsMediaType': 'web',
    'originAuthorName': '搜狐网',
    'emotion': 1}]}]

```



## Client

用途：客户端的登录

```
Client(self, tenant_id, user_id, client_id, client_secret, access_token=None)
```

**Parameters** :

tenant_id - 租户id

user_id - 用户id

client_id - 客户id

client_secret - 客户秘钥

access_token - 访问令牌

**return** :



## Platform

#### 网站账号查询

用途：账号列表查询-网站

```python
Client.platform.get_website(self, **kwargs)
```

**Parameters** :

- Like  - 站点名称模糊查询
- page - 页号，默认值1
- page_size - 每页条目数，默认值10，最大值50

**Return** :

#### 微信账号查询

用途：账号列表查询-微信

```python
Client.platform.get_wechat(self, **kwargs)
```

**Parameters** :

- Like - 站点名称模糊查询
- page - 页号，默认值1
- page_size - 每页条目数，默认值10，最大值50

**Return** :



#### 微博账号查询

用途：账号列表查询-微博

```
Client.platform.get_weibo(self, **kwargs)
```

**Parameters** :

- Like  - 站点名称模糊查询
- page - 页号，默认值1
- page_size -  每页条目数，默认值10，最大值50

**Return** :



#### 区域列表查询

用途：区域列表查询

```
Client.platform.get_area(self, area_id)
```

**Parameters** :

- - area_id - 父级别id，0：表示全国

**return** :



## News

#### 新闻搜索

用途：新闻搜索

```python
Client.news.search(self, latest_days, **kwargs)
```

**Parameters** :

- account_ids - 帐号id集合（站点、微博、微信帐号id）,最多支持传递50个, Set<String>类型
- location_names - 线索地域 线索地域，不传递表示不限制地域,最多支持传递50个, Set<String>类型
- media_types -  媒体类型：对应关系 网站:0, 微博:1, 微信:2, Set<String>类型
- content_classifys -  内容分类集合,  Set<String>类型
- title_like - 标题检索内容
- latest_days -  新闻发布天数
- latest_timestamp - 最大时间戳
- page - 页号，默认值1
- page_size - 每页条目数，默认值10，最大值50

**Retrun** :



#### 新闻详情获取

用途：新闻详情获取

```
Client.news.get_detail(self, resource_id)
```

**Parameters** :

- resource_id - 新闻的id

**return** :



## Tracker

#### 创建事件跟踪

用途：

```python
Client.tracker.create(self, tracker_type, tracker_name, contain_words, exclude_words=None)
```

**Parameters** :

- tracker_type - 事件跟踪类型(1:人物,2:机构,3:产品,4:品牌,5:事件,6:其他)
- tracker_name - 事件名称
- contain_words - 检测词(自定义事件的监测词,用逗号分隔,逗号之间是或的关系,如[a+b+c,d+e],词组1中a+b+c是AND关系，词组2中d+e是AND关系，词组1和词组2是OR关系)
- exclude_words - 排除词集合(自定义事件的排除词,用逗号分隔,逗号之间是或的关系,如fff,ggg,hhh)

**return** :



#### 事件跟踪列表查询

用途：事件跟踪列表查询

```python
Client.tracker.list(self, **kwargs)
```

**Parameters** :

- page - 页号，默认值1
- page_size - 每页条目数，默认值10

**return** :



#### 删除事件跟踪

用途：删除事件跟踪

```
Client.tracker.delete(self, tracker_id)
```

**Parameters** :

- tracker_id - 事件跟踪的id

**return** :



#### 查询新闻汇总接口

用途：查询新闻汇总接口

```
Client.tracker.get_event_tracker_news(self, tracker_id)
```

**Parameters** :

- tracker_id - 事件跟踪的id

**return** :



#### 获取事件热度趋势

用途：获取事件热度趋势

```
Client.tracker.get_yuqing_trend(self, tracker_id)
```

**Parameters** :

- tracker_id - 事件跟踪的id

**return** :



#### 获取事件文章类型分布

用途：获取事件文章类型分布

```
Client.tracker.get_content_type(self, tracker_id)
```

**Parameters** :

- tracker_id - 事件跟踪的id

**return** :



#### 获取事件的相关热词

用途：获取事件的相关热词

```
Client.tracker.get_hotwords(self, tracker_id)
```

**Parameters** :

- tracker_id - 事件跟踪的id

**return** :



#### 获取事件中媒体传播分布

用途：获取事件中媒体传播分布

```
Client.tracker.get_media(self, tracker_id)
```

**Parameters** :

- tracker_id - 事件跟踪的id

**return** :



#### 获取事件发布热区

用途：获取事件发布热区

```
Client.tracker.get_pub_area(self, tracker_id)
```

**Parameters** :

- tracker_id - 事件跟踪的id

**return** :



#### 获取事件情感属性

用途：获取事件情感属性

```
Client.tracker.get_emotion_attr(self, tracker_id)
```

**Parameters** :

- tracker_id - 事件跟踪的id

**return** :



#### 获取事件类型的基本信息

用途：获取事件类型的基本信息

```
Client.tracker.get_profile(self, tracker_id)
```

**Parameters** :

- tracker_id - 事件跟踪的id

**return** :



#### 获取事件类型的基本信息

用途：获取事件类型的基本信息

```
Client.tracker.get_profile(self, tracker_id)
```

**Parameters** :

- tracker_id - 事件跟踪的id

**return** :



#### 获取事件重要文章

用途：获取事件重要文章

```
Client.tracker.get_important_news(self, tracker_id)
```

**Parameters** :

- tracker_id - 事件跟踪的id

**return** :



#### 获取事件活跃媒体

用途：获取事件活跃媒体

```
Client.tracker.get_active_media(self, tracker_id)
```

**Parameters** :

- tracker_id - 事件跟踪的id

**return** :



#### 获取事件提及热区

用途：获取事件提及热区

```
Client.tracker.get_refer_area(self, tracker_id)
```

**Parameters** :

- tracker_id - 事件跟踪的id

**return** :



#### 获取事件情感趋势

用途：获取事件情感趋势

```
Client.tracker.get_emotion_trend(self, tracker_id)
```

**Parameters** :

- tracker_id - 事件跟踪的id

**return** :



#### 获取事件文章列表

用途：获取事件文章列表

```
Client.tracker.get_event_news(self, tracker_id)
```

**Parameters** :

- tracker_id - 事件跟踪的id

**return** :



#### 获取事件文章详情

用途：获取事件文章详情

```
Client.tracker.get_event_news_detail(self, tracker_id, news_uuid)
```

**Parameters** :

- tracker_id - 事件跟踪的id
- news_uuid - 新闻的id

**return** :



## Hotspot

#### 获取热点列表

用途：获取热点列表

```python
Client.hotspot.list(self, sort_name, sort_type, **kwargs)
```

**Parameters** :

- sort_name - 排序字段(poi:热度,posttime:文章发布时间)
- sort_type - 排序规则(desc:降序,asc:升序) 默认值：desc
- category_id - 事件分类id
- scroll_id - 上次查询获取的最新游标
- location - 热点地域，地域标签/河北省/石家庄市
- full_text - 全文检索内容，检索字段，title、summary
- time_start - 热点开始时间 格式 yyyy-MM-dd HH:mm:ss
- time_end - 热点结束时间 格式 yyyy-MM-dd HH:mm:ss
- size - 每次获取条目数，默认值10

**return** :



#### 获取热点类型

用途：获取热点类型

```python
Client.hotspot.get_classify(self)
```

**return** :



#### 地域热点地图统计

用途：地域热点地图统计

```python
Client.hotspot.get_area_heat(self, **kwargs)
```

**Parameters** :

- area_id - 地域id，不传默认传递0，即查询全国各省，传递指定areaId，默认查询下一级的地域的当天数据量统计
- latest_days - 发布时间天数

**return** :



#### 热词排行列表

用途：热词排行列表

```python
Client.hotspot.get_hotwords(self, latest_days, **kwargs)
```

**Parameters** :

- content_classify_id - 内容分类id，不传返回所有
- top_num - 请求条数
- latest_days - 发布时间天数
- location - 提及地域名称

**return** :



## Spread 

#### 批量创建分析任务

用途：批量创建分析任务

```python
Client.spread.create(self, origin_id, title, content)
```

**Parameters** :

- origin_id - 外系统id
- title - 文章标题
- content - 文章正文

**return** :



#### 批量查询任务结果

用途：批量查询任务结果

```python
Client.spread.get_detail(self, task_id)
```

**Parameters** :

- task_id - 任务id，多个以,分隔

**return** :



#### 单篇文章传播分析查询

用途：单篇文章传播分析查询

```
Client.spread.get_analysis(self, title, **kwargs)
```

**Parameters** :

- title - 文章标题
- content - 文章正文

**return** :



## Rank

#### 热搜榜单

用途：热搜榜单

```python
Client.rank.get_hotsearch(self, site_id, classify, **kwargs)
```

**Parameters** :

- site_id - 热搜站点名称，可选360_so 、baidu_so 、sogou_so
- classify - 热搜榜数据类型  详见目录4对照表
- size - 返回的条目数，默认值10条

**return** :



#### 微信榜单

用途：微信榜单

```python
Client.rank.get_wechat(self, sort_name, sort_type, **kwargs)
```

**Parameters** :

- billboard_time_type - 日榜(day)、周榜(week)、月榜(month)
- billboard_time - 榜单时间，格式yyyy-dd-MM

- classify_id - 分类id
- name_like - 模糊查询公众号
- location - 热点地域，地域标签/河北省/石家庄市
- scroll_id - Scroll分页id
- size - 每次获取条目数，默认值10
- sort_name - 排序字段(poi:热度,posttime:文章发布时间)
- sort_type - 排序规则(desc:降序,asc:升序) 默认值：desc

**return** :



#### 微博榜单

用途：微博榜单

```python
Client.rank.get_weibo(self, sort_name, sort_type, **kwargs)
```

**Parameters** :

- billboard_time_type - 日榜(day)、周榜(week)、月榜(month)
- billboard_time - 榜单时间，格式yyyy-dd-MM

- name_like - 模糊查询公众号
- location - 热点地域，地域标签/河北省/石家庄市
- scroll_id - Scroll分页id
- size - 每次获取条目数，默认值10
- sort_name - 排序字段(poi:热度,posttime:文章发布时间)
- sort_type - 排序规则(desc:降序,asc:升序) 默认值：desc

**return** :



#### 头条榜单

用途：头条榜单

```python
Client.rank.get_toutiao(self, sort_name,sort_type, latest_days, **kwargs )
```

**Parameters** :

- billboard_time_type - 日榜(day)、周榜(week)、月榜(month)
- billboard_type - 头条榜单类型--0:媒体,1:自媒体,2:视频
- latest_days - 发布时长
- name_like - 支持模糊查询（支持字段：nickName 和uid）
- scroll_id - scroll分页id
- size - 每次获取条目数，默认值10
- sort_name - 排序字段(poi:热度,posttime:文章发布时间)
- sort_type - 排序规则(desc:降序,asc:升序)默认值：desc

**return** :




































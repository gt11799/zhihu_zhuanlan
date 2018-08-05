知乎专栏API
===

[Toc]

## 总体说明

签名文档见`docs/sign.md`

为了增加返回结果的统一性，结果包含了两部分，`lastUpdate`目前基本是当前时间，用来增量更新(目前用的是id)

数据都放在了`data`里

## 获取有数据的月份

`GET /months`

参数：无

正常时返回

```json
{
    "data": [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8
    ],
    "lastUpdate": 1533453010
}
```


## 获取文章列表

`GET /articles`

参数

| 参数名     | 是否必填    | 说明                         |
|-----------|------------|----------------------       |
| month     | 否         | 月份，不传则是全部的数据        |
| last_id   | 否         | 本地数据中最大的articleId      |

正常时返回

```json
{
    "data": [
        {
            "articleId": 27,
            "commentsCount": 1,
            "date": "20150129",
            "likesCount": 8,
            "title": "《文明之光》之《发明365》-1月29日，椅子的发明",
            "titleImage": "http://7xpxh4.com1.z0.glb.clouddn.com/8c25d0a6-80f9-11e7-8c5a-28cfe91ed6bd",
            "url": "http://zhuanlan.zhihu.com/p/19945855"
        },
        {
            "articleId": 28,
            "commentsCount": 3,
            "date": "20150130",
            "likesCount": 15,
            "title": "​《文明之光》之《发明365#》1月30日- 盛器的发明（1）－陶器",
            "titleImage": "http://7xpxh4.com1.z0.glb.clouddn.com/8c10871c-80f9-11e7-a6df-28cfe91ed6bd",
            "url": "http://zhuanlan.zhihu.com/p/19945880"
        },
        {
            "articleId": 29,
            "commentsCount": 1,
            "date": "20150131",
            "likesCount": 11,
            "title": "​《文明之光》之《发明365》1月31日， 盛器的发明（2）－上釉的发明",
            "titleImage": "http://7xpxh4.com1.z0.glb.clouddn.com/8bd9439e-80f9-11e7-b253-28cfe91ed6bd",
            "url": "http://zhuanlan.zhihu.com/p/19946491"
        }
    ],
    "lastUpdate": 1533452360
}
```


## 获取文章题图列表

`GET /article/images`

>忘了为啥要这个接口了，感觉没用

参数

| 参数名     | 是否必填    | 说明                         |
|-----------|------------|----------------------       |
| month     | 否         | 月份，不传则是一月份的数据       |
| last_id   | 否         | 本地数据中最大的articleId      |

正常时返回

```json
{
    "data": [
        "http://7xpxh4.com1.z0.glb.clouddn.com/996642b3-80f9-11e7-9d58-28cfe91ed6bd",
        "http://7xpxh4.com1.z0.glb.clouddn.com/98c69f7a-80f9-11e7-9bcc-28cfe91ed6bd",
        "http://7xpxh4.com1.z0.glb.clouddn.com/989c71c7-80f9-11e7-99bd-28cfe91ed6bd",
        "http://7xpxh4.com1.z0.glb.clouddn.com/98070461-80f9-11e7-9b33-28cfe91ed6bd",
        "http://7xpxh4.com1.z0.glb.clouddn.com/97b560f8-80f9-11e7-9da6-28cfe91ed6bd",
        "http://7xpxh4.com1.z0.glb.clouddn.com/8c25d0a6-80f9-11e7-8c5a-28cfe91ed6bd",
        "http://7xpxh4.com1.z0.glb.clouddn.com/8c10871c-80f9-11e7-a6df-28cfe91ed6bd",
        "http://7xpxh4.com1.z0.glb.clouddn.com/8bd9439e-80f9-11e7-b253-28cfe91ed6bd"
    ],
    "lastUpdate": 1533453094
}
```

## 健康检查接口

>实际上返回的是client的header信息，后端预留

`GET /_internal/health`

```json
{
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "localhost:5005",
    "Postman-Token": "2d48aca0-724a-402e-a579-9b171183d47c",
    "User-Agent": "PostmanRuntime/7.2.0"
}
```

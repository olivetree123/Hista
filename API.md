# Hista API

## 01. bucket 创建
```
POST    /api/bucket
args    name, public(可选，int, default 0), info(可选)
return
{
    "code": 0,
    "message": null,
    "data": {
        "id": 1,
        "status": 1,
        "create_time": "2018-04-04T14:43:21.400810Z",
        "name": "good",
        "path": "/Users/gao/hista/good",
        "info": "hello",
        "public": 1
    }
}
```
## 02. bucket 更新
```
POST    /api/bucket
args    name, public(可选), info(可选)
return
{
    "code": 0,
    "message": null,
    "data": {
        "id": 1,
        "status": 1,
        "create_time": "2018-04-04T14:43:21.000000Z",
        "name": "good",
        "path": "/Users/gao/hista/good",
        "info": "morning",
        "public": 1
    }
}
```
## 03. bucket 详情
```
GET     /api/bucket
args    name
return
{
    "code": 0,
    "message": null,
    "data": {
        "id": 1,
        "status": 1,
        "create_time": "2018-04-04T14:43:21.400810Z",
        "name": "good",
        "path": "/Users/gao/hista/good",
        "info": "hello",
        "public": 1
    }
}
```
## 04. bucket 删除
```
DELETE      /api/bucket
args        name
return
{
    "code": 0,
    "message": null,
    "data": None
}
```
## 05. bucket 列表
```
GET     /api/bucket/list
args    无
return
{
    "code": 0,
    "message": null,
    "data": [
        {
            "id": 1,
            "status": 1,
            "create_time": "2018-04-04T14:43:21.000000Z",
            "name": "good",
            "path": "/Users/gao/hista/good",
            "info": "morning",
            "public": 1
        }
    ]
}
```
## 06. object 创建/更新
```
POST    /api/object
args    name, bucket, file, info(可选)
return
{
    "code": 0,
    "message": null,
    "data": {
        "id": 1,
        "status": 1,
        "create_time": "2018-04-04T14:47:20.753876Z",
        "name": "pic",
        "info": "good haha",
        "bucket": "good",
        "filename": "nixiongwo.png",
        "md5_hash": "39e16dff5e1a8bb200b138a30de1ffdf"
    }
}
```
## 07. object 详情
```
GET     /api/object
args    name, bucket
return
{
    "code": 0,
    "message": null,
    "data": {
        "id": 1,
        "status": 1,
        "create_time": "2018-04-04T14:47:20.753876Z",
        "name": "pic",
        "info": "good haha",
        "bucket": "good",
        "filename": "nixiongwo.png",
        "md5_hash": "39e16dff5e1a8bb200b138a30de1ffdf"
    }
}
```
## 08. object 列表
```
GET     /api/object/list
args    bucket
return
{
    "code": 0,
    "message": null,
    "data": [
        {
            "id": 1,
            "status": 1,
            "create_time": "2018-04-04T14:47:21.000000Z",
            "name": "pic",
            "info": "good haha",
            "bucket": "good",
            "filename": "nixiongwo.png",
            "md5_hash": "39e16dff5e1a8bb200b138a30de1ffdf"
        }
    ]
}
```
## 09. object 下载
```
GET     /api/object/download
args    bucket, name
return
下载文件
```
## 10. object 删除
```
DELETE      /api/object
args        bucket, name
return
{
    "code": 0,
    "message": null,
    "data": None
}
```
## 11. object 批量删除
```
DELETE      /api/object
args        bucket, name_list
return
{
    "code": 0,
    "message": null,
    "data": None
}
```

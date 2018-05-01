# Hista API

## 01. bucket 创建
```
POST    /api/bucket
args    name, public(可选，int, default 0), desc(可选)  // 可以添加自定义字段
```
## 02. bucket 更新
```
POST    /api/bucket
args    name, public(可选), desc(可选)
```
## 03. bucket 详情
```
GET     /api/bucket
args    name
```
## 04. bucket 删除
```
DELETE      /api/bucket
args        name
```
## 05. bucket 列表
```
GET     /api/bucket/list
args    无
```
## 06. object 创建/更新
```
POST    /api/object
args    name, bucket, file, desc(可选)    //可以添加自定义字段
```
## 07. object 详情
```
GET     /api/object
args    name, bucket
```
## 08. object 列表
```
GET     /api/object/list
args    bucket                          // 参数中可以添加自定义字段，比如 type=image
```
## 09. object 下载
```
GET     /api/object/download
args    bucket, name
```
## 10. object 删除
```
DELETE      /api/object
args        bucket, name
```
## 11. object 批量删除
```
DELETE      /api/object
args        bucket, name_list
```

# 保利云产品平台

[TOC]

## 罗列有调研项目的所有城市名

### HTTP请求

```
GET /city/list
```

### 响应参数

|  参数名   |     参数类型     |  参数描述   |  可空  |
| :----: | :----------: | :-----: | :--: |
| count  |    NUMBER    |  城市数量   |  NO  |
| result | LIST<STRING> | 城市名按字典序 |  NO  |

## 近期开盘项目

### HTTP请求

	GET /property/list
### 参数说明

| 参数名  |  参数类型  | 参数描述 |  可空  |
| :--: | :----: | :--: | :--: |
| city | STRING | 城市名称 |  NO  |

### 响应参数

|    参数名     |      参数类型      |    参数描述     |  可空  |
| :--------: | :------------: | :---------: | :--: |
|   count    |     NUMBER     |    项目数量     |  NO  |
| properties | LIST<PROPERTY> | 项目列表按开盘时间排序 |  NO  |

#### PROPERTY结构

| 参数名            | 参数类型         | 参数描述   | 可空   |
| -------------- | ------------ | ------ | ---- |
| id             | STRING       | 项目ID   | NO   |
| name           | STRING       | 项目名称   | NO   |
| image          | LIST<STRING>       | 项目图片   | NO   |
| description    | STRING       | 项目描述   | NO   |
| location       | STRING       | 项目位置   | NO   |
| open_time_from | TIMESTAMP    | 预计开盘时间 | NO   |
| open_time_to   | TIMESTAMP    | 预计开盘时间 | NO   |
| property_age   | NUMBER       | 产权年限   | NO   |
| surrounding    | LIST<STRING> | 周边配套设施 | NO   |

## 项目可选户型

### HTTP请求

	GET /structure/list

### 参数说明

|     参数名      |  参数类型  | 参数描述  |  可空  |
| :----------: | :----: | :---: | :--: |
|   user_id    | STRING | 用户id  | YES  |
| property_id  | STRING | 项目id  | YES  |
|  room_count  | NUMBER | 房间数目  | YES  |
|  hall_count  | NUMBER | 厅的数目  | YES  |
| toilet_count | NUMBER | 卫生间数目 | YES  |
| lower_limit  | NUMBER | 最小面积  | YES  |
| upper_limit  | NUMBER | 最大面积  | YES  |
|     page     | NUMBER | 默认为1  | YES  |
|    count     | NUMBER | 默认为20 | YES  |

### 响应参数

|    参数名     |   参数类型   |         参数描述          |  可空  |
| :--------: | :------: | :-------------------: | :--: |
| structures |   DICT   | count和LIST<STRUCTURE> |  NO  |
|  property  | PROPERTY |      用于用户查看自己的户型      | YES  |

#### STRUCTURE结构

|     参数名      |  参数类型  | 参数描述  |  可空  |
| :----------: | :----: | :---: | :--: |
|      id      | STRING | 户型id  |  NO  |
|     name     | STRING | 户型名称  |  NO  |
|     area     | NUMBER |  面积   |  NO  |
|    image     | STRING | 户型图片  |  NO  |
|  room_count  | NUMBER | 房间数据  |  NO  |
|  hall_count  | NUMBER | 厅的数目  |  NO  |
| toilet_count | NUMBER | 卫生间数目 |  NO  |

## 项目户型可选的过滤条件

### HTTP请求

```
GET /structure/filter
```

### 参数说明

|     参数名     |  参数类型  |        参数描述         |  可空  |
| :---------: | :----: | :-----------------: | :--: |
| property_id | STRING | 项目id，无此参数时会罗列所有的户型。 | YES  |

### 响应参数

INTERVAL由一个最小值和最大值构成，用来表示一个前开后闭的区间，－1表示无穷大。

TRIPLET是一个三元组分别表示房厅卫的数目。

|       参数名        |      参数类型      |                   参数描述                   |  可空  |
| :--------------: | :------------: | :--------------------------------------: | :--: |
|   area_filter    | LIST<INTERVAL> |                面积,－1代表无穷大                |  NO  |
| structure_filter | LIST<TRIPLET>  | 户型列表(room_count,  hall_count, toilet_count) |  NO  |

## 户型详情

### HTTP请求

```
GET /structure/detail
```

### 参数说明

|     参数名      |  参数类型  | 参数描述 |  可空  |
| :----------: | :----: | :--: | :--: |
| structure_id | STRING | 户型id |  NO  |

### 响应参数

|        参数名         |  参数类型  |      参数描述       |  可空  |
| :----------------: | :----: | :-------------: | :--: |
|        name        | STRING |      户型名称       |  NO  |
|        area        | NUMBER |       面积        |  NO  |
|       image        | STRING |      户型图片       |  NO  |
|     room_count     | NUMBER |      房间数据       |  NO  |
|     hall_count     | NUMBER |      厅的数目       |  NO  |
|    toilet_count    | NUMBER |      卫生间数目      |  NO  |
|     hall_image     | STRING |     客厅图片链接      |  NO  |
| dinning_hall_image | STRING |     餐厅图片链接      |  NO  |
|   bedroom_image    | STRING |     卧室图片链接      |  NO  |
|    toilet_image    | STRING |     卧室图片链接      |  NO  |
|   position_image   | STRING |     位置图片链接      |  NO  |
|    sketchfab_id    | STRING | 在sketchfab网站的id |  NO  |

## 提交评价

### HTTP请求

```
POST /structure/comment
```

### 参数说明

|     参数名      |  参数类型  | 参数描述 |  可空  |
| :----------: | :----: | :--: | :--: |
| property_id  | STRING | 项目id | YES  |
| structure_id | STRING | 户型id |  NO  |

### POST数据



|      key       | value类型 |   说明   |  可空  |
| :------------: | :-----: | :----: | :--: |
|    user_id     | STRING  | 评论用户ID | YES  |
|     phone      | STRING  |  电话号码  | YES  |
|     title      | STRING  |   称谓   | YES  |
| estimated_time | STRING  | 计划购买时间 | YES  |
|    comment     |  DICT   |  用户评论  |  NO  |

#### COMMENT结构

|         参数名          |  参数类型  | 参数描述  |  可空  |
| :------------------: | :----: | :---: | :--: |
|      hall_score      | NUMBER | 客厅评分  |  NO  |
|     hall_comment     | STRING | 客厅评价  |  NO  |
|  dinning_hall_score  | NUMBER | 餐厅评分  |  NO  |
| dinning_hall_comment | STRING | 餐厅评价  |  NO  |
|    bedroom_score     | NUMBER | 卧室评分  |  NO  |
|   bedroom_comment    | STRING | 卧室评价  |  NO  |
|     toilet_score     | NUMBER | 卫生间评分 |  NO  |
|    toilet_comment    | STRING | 卫生间评价 |  NO  |
|    overview_score    | NUMBER | 综合评分  |  NO  |
|   overview_comment   | STRING | 综合评价  |  NO  |

### 响应参数

|  参数名   |  参数类型  | 参数描述 |  可空  |
| :----: | :----: | :--: | :--: |
| status | STRING | 返回状态 |  NO  |

## 添加或更新用户基本信息

```sdf
POST /user/infomation/set
```

### 参数说明

|       参数名        |  参数类型  | 参数描述  |  可空  |
| :--------------: | :----: | :---: | :--: |
|     user_id      | STRING | 用户ID  |  NO  |
|      phone       | STRING | 电话号码  | YES  |
|    weixin_id     | STRING | 微信ID  |  NO  |
| family_structure | NUMBER | 家庭结构  | YES  |
|   income_lower   | NUMBER | 最低年收入 | YES  |
|   income_upper   | NUMBER | 最高年收入 | YES  |
|    occupation    | STRING |  职业   | YES  |
|    education     | STRING | 教育程度  | YES  |
|       age        | NUMBER | 当前年龄  | YES  |
|  purchase_times  | NUMBER | 置业次数  | YES  |

### 响应参数

|  参数名   |  参数类型  | 参数描述 |  可空  |
| :----: | :----: | :--: | :--: |
| status | STRING | 返回状态 |  NO  |

## 用户的户型信息

```sdf
GET /user/structure/get
```

### 参数说明

|   参数名   |  参数类型  | 参数描述 |  可空  |
| :-----: | :----: | :--: | :--: |
| user_id | STRING | 用户id |  NO  |

### 响应参数

|    参数名    |   参数类型    |  参数描述   |  可空  |
| :-------: | :-------: | :-----: | :--: |
| property  | PROPERTY  |  项目信息   |  NO  |
| structure | STRUCTURE |  户型信息   |  NO  |
|  comment  |  COMMENT  | 对该户型的评价 |  NO  |

## 

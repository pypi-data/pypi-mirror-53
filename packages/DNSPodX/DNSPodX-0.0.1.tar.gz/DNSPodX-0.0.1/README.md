# DNSPodX

![Windows](https://img.shields.io/badge/Windows-support-green.svg)
![Linux](https://img.shields.io/badge/Linux-support-green.svg)
![License](https://img.shields.io/badge/License-MPL_2.0-orange.svg)
![Python](https://img.shields.io/badge/Python-3.7-blue.svg)
![Version](https://img.shields.io/badge/Version-1.x-blueviolet.svg)

采用面向对象的方式封装DNSPod官方API，尽可能降低调用API的成本，根据官方v4.6版本API开发。

新手上路，请多指教。若有需要请联系我：mailto@wolfbolin.com



## 完成进度

| 功能点 |  进度 |
| ------ | ---- |
|**帐户相关**|xxxxx|
|获取帐户信息|*计划中*|
|修改资料||
|修改密码||
|修改邮箱||
|获取手机验证码||
|获取用户日志|*计划中*|
|获取API版本号|**已完成**|
|**域名相关**|xxxxx|
|添加新域名|*计划中*|
|获取域名列表|**已完成**|
|删除域名|*计划中*|
|设置域名状态|*计划中*|
|获取域名信息||
|获取域名日志||
|设置搜索引擎推送||
|添加域名共享||
|域名共享列表||
|修改域名共享||
|删除域名共享||
|域名过户||
|锁定域名||
|域名锁定解锁||
|域名绑定列表||
|添加域名绑定||
|删除域名绑定||
|获取域名分组||
|添加域名分组||
|修改域名分组||
|删除域名分组||
|设置域名分组||
|设置域名星标||
|设置域名备注|*计划中*|
|获取域名权限||
|获取等级允许的记录类型||
|获取等级允许的线路||
|**记录相关**|xxxxx|
|添加记录|**已完成**|
|记录列表|**已完成**|
|修改记录|**已完成**|
|删除记录|**已完成**|
|更新动态DNS记录|**已合并**|
|设置记录备注|**已完成**|
|获取记录信息|**已完成**|
|设置记录状态|**已合并**|
|**批量操作**|xxxxx|
|批量添加域名|*计划中*|
|批量添加记录|*计划中*|
|批量修改记录|*计划中*|
|获取任务详情|*计划中*|



## 特别提醒

根据Python编程的特性，我们可以在函数响应时返回多个值。因此本Pypi包在响应函数调用时均采用返回两个值的方式，第一个返回值为具体的数值或对象，第二个返回值为API调用后响应的Json数据（已转字典）。

如果文档有不完善之处还请多多包涵，欢迎参考参考示例、阅读源码、提Issue、发邮件。感恩~



## 账户相关

### 用户对象

**`__init__(self, user_id, token)`**

声明该对象需要传入用户在平台上申请的id与token以组合为调用API的key。

该操作可完成用户对象的创建，为后续的所有操作提供访问凭证。id与token的获取请参考官方文档。

```python
user = DNSPodX.User(user_id, token)
```

### 版本信息

**`version(self)`**

该操作可返回线上的API版本

```python
api_version = user.version()
print(api_version)
```

### 获取域名列表

**`domain_list(self, offset=0, length=50, domain_type=None, group_id=None, keyword=None)`**

该操作虽然在域名API列表中，但是因为其与用户信息关系紧密，所以放置于用户类下。该函数的第一个返回值是一个包含域名对象的列表。

```python
user = DNSPodX.User(user_id, token)
domain_list = user.domain_list()[0]
```

## 域名相关

### 域名对象

**`__init__(self, user, name)`**

声明该对象需要传入用户对象和一个域名，该参数将初始化一个域名对象的必要信息。

该操作可完成域名对象的创建，之后可使用此对象修改域名的相关信息。

```python
user = DNSPodX.User(user_id, token)
domain = DNSPodX.Domain(user, 'example.com')
```

### 获取记录列表

**`record_list(self, offset=0, length=2000, sub_domain=None, record_type=None, record_line=None, keyword=None)`**

该操作虽然在记录API列表中，但是因为其与域名信息关系紧密，所以放置于域名类下。该函数的第一个返回值是一个包含记录对象的列表。

```python
user = DNSPodX.User(user_id, token)
domain = DNSPodX.Domain(user, 'example.com')
record_list = domain.record_list()[0]
```

## 记录相关

### 记录对象

**`__init__(self, user, domain, name, r_type, value, line=None, ttl=None, mx=None, r_id=None, status=None)`**

声明该对象需要传入用户对象和域名对象，该参数将初始化一个记录对象的必要信息。

同时你还需要传入一些必要的数据来初始化对象，我们认为每个记录都不应该是空的。

```python
user = DNSPodX.User(user_id, token)
domain = DNSPodX.Domain(user, 'example.com')
record = DNSPodX(user, domain, 'www', 'A', '127.0.0.1')
```

### 查看信息

**`detail(self)`**

此方法区别于`info()`，此函数仅返回对象中存储的存储数据。不会通过API更新对象的信息。

### 创建记录

**`create(self)`**

此方法将根据对象属性通过API接口创建DNS记录，此时请勿携带record_id参数。

### 修改记录

**`modify(self)`**

此方法将根据对象属性通过API接口修改DNS记录，此时请携带record_id参数。

### 删除记录

**`remove(self)`**

此方法将根据对象属性通过API接口删除DNS记录，此时仅携带record_id参数即可。

### 添加备注

**`remark(self, remark)`**

此方法将通过API接口创建DNS记录备注，此时仅携带record_id参数即可。

### 获取信息

**`info(self, r_id)`**

此方法将通过API接口获取DNS记录信息，此时仅携带record_id参数即可。




百度sdk

# 安装
```
pip install baidu-api
```

# 文档
```
# 授权认证
>>> from baidu.client import BaiduClient
>>> client = BaiduClient(app_id=<你的appid>, api_key=<你的apikey>, secret_key=<你的secretkey>)
# 调用接口
>>> from baidu.api import TextCensor
>>> result, detail = TextCensor(client).is_allowed("在线阅读色情小说,在线赌博,枪支弹药购买: https://iqiyi.com")
>>> result == "rejected"
True
```
## 使用redis缓存`access_token`
```
from redis import Redis
from baidu.session.redisstorage import RedisStorage
redis_client = Redis.from_url("redis://localhost:6379/0")
session_interface = RedisStorage(redis_client, prefix="baiduapi")
baidu_client = BaiduClient(app_id, api_key, secret_key,
                           session=session_interface)
```

# 感谢
* 里面的session是模仿的[wechatpy](https://github.com/jxtech/wechatpy)的session

# 贡献代码
欢迎提交pr, 我一定会尽早地处理. 不用在乎什么格式, 写代码就是勇敢地提交, 上线. 出错了再修改, 回滚就可以了啊.

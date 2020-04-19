# 框架文档



[TOC]

# 00 Service Controller 使用



## 00.1 共享内存

在工作进程池中提供了一些 service 可共享的工具，在service 中作为第一个参数使用

```python
class CommonTools:

    def __init__(self):
        self.mem_cache = None # 未来成为 MemCacheMultiProcess 或 MemCacheSingletonProcess
        
class WorkerPool:

    def __init__(self, mode=None):
        # ...
    	self.common_tools = CommonTools() # service中传递的controler是worker pool 的这个东西
        # ...
```



`MemCacheMultiProcess`封装了`multiprocessing.Manager().dict()`,提供进程间的数据同步

详情见 `memcache.py`

```python
class MemCacheMultiProcess:

    def __init__(self):
        pass

    def lock_key(self, key):
        pass

    def unlock_key(self, key):
        pass

    def set(self, key, val):
        pass

    def get(self, key):
        pass

    def compare_and_set(self, key, except_val, set_val):
        pass
```





## 00.2 单服务器 service 之间的调用



首先是数据包格式 `[消息长度][消息句柄][消息体]`。消息句柄是全局唯一的整数值，决定了该数据包会有哪一个service处理。

框架网络IO模块收好数据包后，会调用五个函数。

```python
    def run(self, controller, req, res):
        try:
            self.system_pretreatment(req, res)				# [1]
            if callable(self.pre_handler):					
                self.pre_handler(controller, req, res)		# [2]
            self.handler(controller, req, res)				# [3]
            if callable(self.last_handler):					
                self.last_handler(controller, req, res)		# [4]
            self.system_aftertreatment(req, res)			# [5]
        except Exception as e:
            # log something
```

其中 `req和 res`描述了 request和response的所有过程

- 在函数一。会对`req`中消息的消息体按照request中的序列化方法进行反序列化. 变成python 中的字典。存在`req.content`
- 函数二到四有用户定义。要求在最后把`res.content`设置为python的字典
- 函数五会对上述`res.content`序列化成字符流。构建成能发的包。

service内调用我希望省去包的序列化。输入一个字典，返回一个字典

例子

```python
res_dict = 
controller.handler_dict[config.USER_REGISTER_SERVICE].inline_call(controller, {
    "username": "cwl",
    "password": "123456"
})

res_dict = 
controller.handler_dict[需要调用的service id].inline_call(controller, {
    "username": "cwl",
    "password": "123456"
})
```
本质是`inline_call`只调用了上面中间三个用户定义函数。



## 00.3 延时事件的使用



```python
    controller.events.start_delay_event(DelayEvent(
        config.GAME_MGR_PLAY_WITH_OTHERS_SERVICE,
        {
            "user_id": user_id,
            "matching_time": matching_time,
            "mode": mode
        },
        2	# 单位 秒 浮点数
    ))
```


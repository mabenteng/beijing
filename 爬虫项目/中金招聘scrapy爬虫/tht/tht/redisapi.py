import redis    # 导入redis 模块

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)  
r.set('name', 'runoob')  # 设置 name 对应的值
print(r.get('name'))  # 取出键 name 对应的值
# r.exists(name) 是否存在某个key
# r.rpush("tht","url")
# r.rpush("tht","url2")
# r.rpush("tht","url3")
# r.rpush("tht","url4")

# /设置集合的url,集合不允许url重复
# r.sadd("benty","url1")
# r.sadd("benty","url4")
# r.sadd("benty","url5")
# r.sadd("benty","url8")
# r.sadd("benty","url9")
# 获取所有的集合成员
# print(r.smembers('benty')) #获取所有集合的元素
# print(r.scard('benty')) # 获取集合元素的个数
# print(r.sismember('benty',"url8")) # 检查xxx是否在集合内
# print(r.sismember('benty',"url00")) # 检查xxx是否在集合内,说白了就是元素是否存在




#!/usr/bin/python
# -*- coding: UTF-8 -*-
import redis

# 连接redis
def get_redis_cli():
    redis_cli = redis.Redis(host='127.0.0.1', port=6379, db=1, decode_responses=True)
    return redis_cli

# 进行reids list lpush操作
def set_redis_list_lpush(name,value):
    rdb = get_redis_cli()
    return rdb.lpush(name,value)

# 进行reids list rpop操作
def get_redis_list_rpop(name):
    rdb = get_redis_cli()
    return rdb.rpop(name)

# 进行reids list lrange操作
def get_redis_list_lrange(name,start,end):
    rdb = get_redis_cli()
    return rdb.lrange(name,start,end)

# 进行reids list llen操作
def get_redis_list_llen(name):
    rdb = get_redis_cli()
    return rdb.llen(name)
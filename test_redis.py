#!/usr/bin/python
# -*- coding: UTF-8 -*-

from rdb import set_redis_list_lpush

set_redis_list_lpush('rag:urls','https://lilianweng.github.io/posts/2023-06-23-agent')
set_redis_list_lpush('rag:urls','https://python.langchain.com.cn/docs/get_started/introduction')
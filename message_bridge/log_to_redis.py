#!/usr/bin/python
from RedisQueue import RedisQueue
import subprocess
import json
import base64
import sys

q = RedisQueue(sys.argv[1], namespace='ansible', host='internal-redis.ovmdvp.0001.use2.cache.amazonaws.com', port=6379, db=1)
q.put(json.dumps({'type': sys.argv[2], 'payload': sys.argv[3]}))

#!/usr/bin/python
from RedisQueue import RedisQueue
import subprocess
import json
import base64
import sys

q = RedisQueue(sys.argv[1], namespace='ansible', host='localhost', port=6379, db=0)
q.put(json.dumps({'type': sys.argv[2], 'payload': sys.argv[3]}))

#!/usr/bin/python
import subprocess
import json
import base64
import uuid
import os
import redis

class RedisQueue(object):
    """Simple Queue with Redis Backend"""
    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' %(namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)

q = RedisQueue('messages', namespace='ansible', host='10.0.1.4', port=6379, db=0)
response_id = str(uuid.uuid4())

q.put(json.dumps({
                'job': 'build',
                'build_id': 123,
                'call_id': 1234,
                'action': 'run_playbook',
                'playbook': 'deploy',
                'response_id': response_id,
                'environment': 'qa',
                'service': 'configuration-ms',
                'image': 'srkay-on.azurecr.io/services/configuration-ms',
                'git_commit': os.environ['GIT_COMMIT'],
                'port': 3031,
                #extra vars
                'alpha': 1,
                'beta': 2
        }))

q = RedisQueue(response_id, namespace='ansible', host='10.0.1.4', port=6379, db=0)

while True:
        log = q.get()
        message = json.loads(log)
        if message['type'] == 'end':
                break
        else:
                print message['payload']

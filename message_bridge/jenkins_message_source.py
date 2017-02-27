#!/usr/bin/python
from RedisQueue import RedisQueue
import subprocess
import json
import base64
import uuid

q = RedisQueue('messages', namespace='ansible', host='localhost', port=6379, db=0)
response_id = str(uuid.uuid4())

q.put(json.dumps({
                'job': 'build',
                'build_id': 123,
                'call_id': 1234,
                'action': 'run_playbook',
		'playbook': 'test',
                'with_vars': {
                        'alpha': 1,
                        'beta': 2
                },
		'response_id': response_id
        }))

q = RedisQueue(response_id, namespace='ansible', host='localhost', port=6379, db=0)

while True:
	log = q.get()
	message = json.loads(log)
	if message['type'] == 'end':
		break
	else:
		print message['payload']

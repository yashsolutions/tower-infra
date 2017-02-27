#!/usr/bin/python
from RedisQueue import RedisQueue
import subprocess
import json
import base64

q = RedisQueue('messages', namespace='ansible', host='localhost', port=6379, db=0)

while True:
	res = q.get()
	message = json.loads(res)
	subprocess.Popen(["/home/ashish/messages/run_ansible_controller.sh", message['response_id'], message['playbook'], base64.b64encode(res)])

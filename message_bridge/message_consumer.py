#!/usr/bin/python
from RedisQueue import RedisQueue
import subprocess
import json
import base64

q = RedisQueue('messages', namespace='ansible', host='internal-redis.ovmdvp.0001.use2.cache.amazonaws.com', port=6379, db=1)

while True:
	res = q.get()
	message = json.loads(res)
	subprocess.Popen(["/home/ubuntu/ansible-bot/message_bridge/run_ansible_controller.sh", message['response_id'], message['playbook'], base64.b64encode(res)])

#!/bin/bash

message_json=`echo $3 | base64 --decode`

while read -r line
do
	/home/ubuntu/ansible-bot/message_bridge/log_to_redis.py $1 log "$line"
done < <(cd /home/ubuntu/ansible-bot && ansible-playbook --vault-password-file /home/ubuntu/.ansible-secret -e "$message_json" "playbooks/$2.yml" 2>&1)

/home/ubuntu/ansible-bot/message_bridge/log_to_redis.py $1 end 0

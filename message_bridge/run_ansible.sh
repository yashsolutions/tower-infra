#!/bin/bash

message_json=`echo $3 | base64 --decode`

while read -r line
do
	/home/ansible/ansible/message_bridge/log_to_redis.py $1 log "$line"
done < <(cd /home/ansible/ansible && ansible-playbook --vault-password-file /home/ansible/.ansible-secret -e "$message_json" "playbooks/$2.yml" 2>&1)

/home/ansible/ansible/message_bridge/log_to_redis.py $1 end 0

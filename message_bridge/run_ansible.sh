#!/bin/bash

message_json=`echo $3 | base64 --decode`

while read -r line
do
	./log_to_redis.py $1 log "$line"
done < <(cd /home/ashish/ansible && ansible-playbook -e "$message_json" "$2.yml" 2>&1)

./log_to_redis.py $1 end 0

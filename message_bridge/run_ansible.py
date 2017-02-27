import sys
import base64
import json

message = json.loads(base64.b64decode(bytes(sys.argv[1],'utf-8')))
print message

with open('/tmp/output.txt','w') as f:
	f.write(message)
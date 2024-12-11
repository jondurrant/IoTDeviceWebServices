import requests
import os
import json
import sys
from datetime import datetime, timedelta



hostname = "localhost"
port = 5000

if len(sys.argv) < 3:
    print("Usage getConfig <device> <type> [<host> <port> <prefix>]")
    sys.exit(0)
    
device = sys.argv[1]
type   = sys.argv[2]
    

if len(sys.argv) >= 4:
    hostname = sys.argv[3]

if len(sys.argv) >= 5:
    port = int(sys.argv[4])
    
if len(sys.argv) >= 6:
    prefix = "/" + sys.argv[5] + "/"
else:
    prefix = "/"


if (port % 1000) == 443:
    url = ('https://%s:%d%sgetConfig'%(hostname, port, prefix))
else:    
    url = ('http://%s:%d%sgetConfig'%(hostname, port, prefix))
newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}




j = {
    "device": device,
    "type": type
    }


x = requests.post(url, json=j, headers=newHeaders)
if (not x.ok):
    print("HTTP ERROR Code %d"%x.status_code)
else:
    t = x.json()
    print(json.dumps(t))

        
        

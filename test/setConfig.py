import requests
import os
import json
import sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine, select, delete, Table, MetaData
import sqlalchemy

sys.path.insert(1, '../src')
from DeviceConfig import DeviceConfig



hostname = "localhost"
port = 5000

if len(sys.argv) < 3:
    print("Usage getConfig <device> <type> [<config>=<value>]")
    sys.exit(0)
    
device = sys.argv[1]
type   = sys.argv[2]


j = {}

for a in range(3, len(sys.argv)):
    (k, s, v) = sys.argv[a].partition("=")
    try:
        v = int(v)
    except:
        try:
            v = float(v)
        except:
            pass
    if v == "true":
        v = True
    if v == "false":
        v = False

    j[k] = v



#setup DB connection 
dbHost=os.environ.get("DB_HOST", "localhost")
dbPort=os.environ.get("DB_PORT", "3306")
dbSchema=os.environ.get("DB_SCHEMA", "root")
dbUser=os.environ.get("DB_USER", "root")
dbPasswd=os.environ.get("DB_PASSWD", "root")
connectString = "mysql+mysqlconnector://%s:%s@%s:%s/%s"%(dbUser, dbPasswd, dbHost, dbPort, dbSchema)
engine = create_engine(connectString)

configTab = DeviceConfig(engine)
configTab.setConfig(device, type, json.dumps(j))

print(json.dumps(j))

        
        

import pandas as pd
from sqlalchemy import create_engine, select, delete, Table, MetaData, desc, func, inspect, insert
import sqlalchemy
import json

class DeviceConfig:
    def __init__(self, dbEng):
        self.dbEng = dbEng
        self.metadata=MetaData()
        
        self.tableName = 'DeviceConfig'
        self.configTable= Table(
            self.tableName, 
            self.metadata,
            sqlalchemy.Column('Device',     sqlalchemy.String(length=40)),
            sqlalchemy.Column('Type',     sqlalchemy.String(length=40)),
            sqlalchemy.Column('ConfigTime',   sqlalchemy.DateTime()),
            sqlalchemy.Column('Config',     sqlalchemy.String(length=1024))
            )
        self.metadata.create_all(self.dbEng)
        
    def getConfig(self, device, type):
        res = self._getConfig(device)
        if res == None:
            self.setConfig(device, type, "{}")
            res = self._getConfig(device)
        return res
        
    def _getConfig(self, device):
        stmt = select(
            self.configTable,
            self.configTable.c.Config
          ).where(
              self.configTable.c.Device == device
          ).order_by(
              desc(self.configTable.c.ConfigTime)
          ).limit(1)
        conn = self.dbEng.connect()
        res = conn.execute(stmt)
        rows = res.all()
        count = len(rows)
        if (count == 0):
            return None
        config = rows[0][3]
        conn.close()
        return config
    
    def setConfig(self, device, type, config):
        stmt = insert(self.configTable).values(
            Device = device,
            Type = type,
            ConfigTime = pd.Timestamp.utcnow(),
            Config = config
            )
        conn = self.dbEng.connect()
        res = conn.execute(stmt)
        conn.commit()
        conn.close()
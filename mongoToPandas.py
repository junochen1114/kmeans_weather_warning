# import pymongo
# import pandas as pd
#
# client = pymongo.MongoClient('mongodb://106.75.143.92:19997/')
# db = client.risk_db
# collection = db.weatherWarning
#
# # 先确认所有warnAct都是发布
# print(collection.find({'warnAct':'发布'}).count()
#       == collection.count() )

# 时间: 半年左右
# 地点 ：全国各地
# 数据：预警颜色，预警类型

import pandas as pd
import os
import sys
from pymongo import MongoClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "./")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))


class mongoToPandas:
    def __init__(self, host, port, db, collection):
        self.mongo_uri = 'mongodb://%s:%s/' % (host, port)
        self.conn = MongoClient(self.mongo_uri)
        self.db = self.conn[db]
        self.col = self.db[collection]
        self.cursor = []
        self.df = pd.DataFrame()

    def read_mongo(self, query={}, no_id=True):
        self.df = pd.DataFrame(self.col.find(query))
        if no_id:
            del self.df['id']
        del self.df['_id']
        return self.df

    def count(self, para='largeLocation'):
        self.cursor = self.col.distinct(para)
        return self.cursor


# if __name__ == '__main__':
#     mp = mongoToPandas('106.75.143.92', '19997', 'risk_db', 'weatherWarning')
#     ct = mp.count('warnColor')
#     cd = mp.read_mongo({'warnColor': '心脑'})
#     print(ct)
#     print(cd)











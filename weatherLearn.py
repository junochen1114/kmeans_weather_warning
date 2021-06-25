import pandas as pd
# import time
import mongoToPandas


# 获取按照地点分类的多个表格
class weatherLearn:
    def __init__(self):
        self.mp = mongoToPandas.mongoToPandas('106.75.143.92', '19997', 'risk_db', 'weatherWarning')
        self.places = sorted(self.mp.count())
        self.data = ['0']*len(self.places)
        self.excelname = r'C:\Users\chenkangyun\PycharmProjects\untitled\weatherLearn.xlsx'
        self.workbook = pd.ExcelWriter(self.excelname, engine='openpyxl')

    def load_data(self):
        for i in range(len(self.places)):
            dt = self.mp.read_mongo({'largeLocation': self.places[i]}, no_id=False).sort_values(by='publishTime')
            del dt['largeLocation']
            self.data[i] = dt
        return self.data

    def write_sheet(self):
        for i in range(len(self.places)):
            self.data[i].to_excel(self.workbook, sheet_name=self.places[i])
        self.workbook.save()


if __name__ == '__main__':
    # time_start = time.time()

    wl = weatherLearn()
    wl.load_data()
    wl.write_sheet()

    # time_end = time.time()
    # time_c = time_end - time_start  # 运行所花时间
    # print('time cost', time_c, 's')

# for place in places:
#     data = mp.read_mongo({'largeLocation': place}, no_id=False).sort_values(by='publishTime')
#



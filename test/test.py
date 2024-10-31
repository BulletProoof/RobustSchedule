import numpy as np
import pandas as pd
import random
from datetime import timedelta

data = [[0, 40, 50, 0, 0, 1236, 0],
        [1, 45, 68, 10, 912, 967, 90],
        [2, 45, 70, 30, 825, 870, 90],
        [3, 42, 66, 10, 65, 146, 90],
        [4, 42, 68, 10, 727, 782, 90],
        [5, 42, 65, 10, 15, 67, 90],
        [6, 40, 69, 20, 621, 702, 90],
        [7, 40, 66, 20, 170, 225, 90],
        [8, 38, 68, 20, 255, 324, 90],
        [9, 38, 70, 10, 534, 605, 90],
        [10, 35, 66, 10, 357, 410, 90],
        [11, 35, 69, 10, 448, 505, 90],
        [12, 25, 85, 20, 652, 721, 90],
        [13, 22, 75, 30, 30, 92, 90],
        [14, 22, 85, 10, 567, 620, 90],
        [15, 20, 80, 40, 384, 429, 90],
        [16, 20, 85, 40, 475, 528, 90],
        [17, 18, 75, 20, 99, 148, 90],
        [18, 15, 75, 20, 179, 254, 90],
        [19, 15, 80, 10, 278, 345, 90],
        [20, 30, 50, 10, 10, 73, 90],
        [21, 30, 52, 40, 914, 965, 90],
        [22, 28, 52, 40, 812, 883, 90],
        [23, 28, 55, 10, 732, 777, 90],
        [24, 25, 50, 10, 65, 144, 90],
        [25, 25, 52, 40, 169, 224, 90],
        [26, 25, 55, 10, 622, 701, 90],
        [27, 23, 52, 10, 261, 316, 90],
        [28, 23, 55, 20, 546, 593, 90],
        [29, 20, 50, 10, 358, 405, 90],
        [30, 20, 55, 10, 449, 504, 90]]
df = pd.DataFrame(data, columns=['CustomerID', 'XCoord', 'YCoord', 'Demand', 'ReadyTime', 'DueTime', 'ServiceTime'])
print(df)
df.to_csv('gurobi_data/customers.csv', index=False)

# 根据XCoord/YCoord生成距离矩阵保留三位小数
distances = np.zeros((len(df), len(df)))
for i in range(len(df)):
    for j in range(len(df)):
        distances[i][j] = np.sqrt((df.loc[i, 'XCoord'] - df.loc[j, 'XCoord']) ** 2 + (df.loc[i, 'YCoord'] - df.loc[j, 'YCoord']) ** 2)
distances = np.round(distances, 3)
print(distances)
# 首行和首列为对应的CustomerID
np.savetxt('gurobi_data/distances.csv', distances, delimiter=',', fmt='%f')


# 按照 SectiontID	Origin	Destination	Interval	Risk 生成内容
# sectionID为


risk_data = []
section_id = 0
interval_nums = 24 # 间隔数
seed = 46
# 根据seed生成30-90的随机数
random.seed(seed)

for i in range(len(df)):
    for j in range(len(df)):
        if i == j : continue
        for k in range(interval_nums):
                risk = random.randint(15, 45)
                if k == 8 or k == 9 or k == 17 or k == 18:
                     risk = random.randint(40, 80)
                risk_data.append(
                     [section_id, i, j, k, 
                      (24 * 60) / interval_nums * k, (24 * 60) / interval_nums * (k + 1), 
                      str(timedelta(minutes=(24 * 60) / interval_nums * k)), str(timedelta(minutes=(24 * 60) / interval_nums * (k + 1))), 
                      risk]
                )
        section_id += 1

df_risk = pd.DataFrame(risk_data, columns=['SectiontID', 'Origin', 'Destination', 'Interval', 'IntetvalStart', 'IntetvalEnd', 'IntetvalStartTime', 'IntetvalEndTime', 'Risk'])
print(df_risk)
df_risk.to_csv('gurobi_data/risk.csv', index=False)




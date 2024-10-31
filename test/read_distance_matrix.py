# 测试utils中的read_distance_matrix函数
# 单元测试
import pandas as pd

def read_distance_matrix(file_path):
    df = pd.read_csv(file_path, header=None)
    distance_matrix = [[0] * len(df) for _ in range(len(df))]
    
    for i in range(len(df)):
        for j in range(len(df)):
            distance_matrix[i][j] = df.iloc[i, j]
    return distance_matrix

distance_matrix = read_distance_matrix("./gurobi_data/distances.csv")
# print(distance_matrix)
print(distance_matrix[0][1])
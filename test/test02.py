import pandas as pd

def read_distance_matrix(file_path):
    df = pd.read_csv(file_path)
    distance_matrix = [[0] * len(df) for _ in range(len(df))]
    
    for i in range(len(df)):
        for j in range(len(df)):
            distance_matrix[i][j] = df.iloc[i, j]
            
    return distance_matrix
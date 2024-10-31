import pandas as pd

# 创建一个简单的DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})

# 使用apply函数将每列的每个元素平方
df_squared = df.apply(lambda x: x**2)

print(df_squared)
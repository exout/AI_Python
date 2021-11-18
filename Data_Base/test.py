import pandas as pd

df = pd.read_csv('comp.csv')
df1 = df.set_index('isin')
df1.to_csv('company_stock.csv', encoding='utf-8')
print(df1.head())
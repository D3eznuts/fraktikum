import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('./dataset/global_ecommerce_sales.csv')
print(df.head())
print(df.info())
print(df.isnull().sum())

df = df[df['Unit_Price'] > 0]
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df['Month'] = df['Order_Date'].dt.to_period('M').astype(str)
monthly_sales = df.groupby('Month')['Total_Sales'].sum()

plt.figure(figsize=(10,5))
plt.plot(monthly_sales.index, monthly_sales.values, marker='o', color='b') # type: ignore
plt.title('Tren Penjualan Bulanan')
plt.xticks(rotation=45)
plt.show()
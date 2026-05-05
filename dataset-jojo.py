import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('./dataset/jojostandstatsv2.csv', encoding='latin1')

print("Data Awal:")
print(df.head())

df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

rank_map = {
    'A': 5,
    'B': 4,
    'C': 3,
    'D': 2,
    'E': 1
}

cols = ['PWR', 'SPD', 'RNG', 'PER', 'PRC', 'DEV']

for col in cols:
    df[col] = df[col].map(rank_map)

print("\nCek nilai null setelah mapping:")
print(df.isnull().sum())

df = df.dropna()

df['Total'] = df[cols].sum(axis=1)

top_stand = df.sort_values(by='Total', ascending=False).head(10)

print("\nTop 10 Stand:")
print(top_stand[['Stand', 'Total']])

plt.figure()
plt.barh(top_stand['Stand'], top_stand['Total'])
plt.gca().invert_yaxis()
plt.title('Top 10 Stand Terkuat')
plt.xlabel('Total Stat')
plt.ylabel('Stand')
plt.show()

df[cols].hist()
plt.suptitle('Distribusi Stat')
plt.show()

correlation = df[cols].corr()

sns.heatmap(correlation, annot=True)
plt.title('Korelasi Antar Stat')
plt.show()

special = df[(df['PWR'] >= 4) & (df['SPD'] <= 2)]

print("\nPower tinggi tapi Speed rendah:")
print(special[['Stand','PWR','SPD']])
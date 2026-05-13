import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('./dataset/jojostandstatsv2.csv', encoding='latin1')

print("===== DATA AWAL =====")
print(df.head())

df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))

rank_map = {
    'A': 5,
    'B': 4,
    'C': 3,
    'D': 2,
    'E': 1
}

cols = ['PWR', 'SPD', 'RNG', 'PER', 'PRC', 'DEV']

for col in cols:
    print(f"\nValue unik kolom {col}:")
    print(df[col].unique())

for col in cols:
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].map(rank_map)

print("\n===== NULL SETELAH MAPPING =====")
print(df[cols].isnull().sum())

df = df.dropna(subset=cols)

for col in cols:
    df[col] = df[col].astype(int)

df['Total'] = df[cols].sum(axis=1)

top_stand = df.sort_values(by='Total', ascending=False).head(10)

print("\n===== TOP 10 STAND =====")
print(top_stand[['Stand', 'Total']])

plt.figure(figsize=(10,6))

plt.barh(top_stand['Stand'], top_stand['Total'])

plt.gca().invert_yaxis()

plt.title('Top 10 Stand Terkuat')
plt.xlabel('Total Stat')
plt.ylabel('Stand')

plt.show()

df[cols].hist(figsize=(12,8))

plt.suptitle('Distribusi Stat')

plt.show()

plt.figure(figsize=(8,6))

correlation = df[cols].corr()

sns.heatmap(
    correlation,
    annot=True,
    cmap='coolwarm'
)

plt.title('Korelasi Antar Stat')

plt.show()

special = df[
    (df['PWR'] >= 4) &
    (df['SPD'] <= 2)
]

print("\n===== POWER TINGGI TAPI SPEED RENDAH =====")
print(special[['Stand', 'PWR', 'SPD']])
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('./dataset/Dragon_Ball_Data_Set.csv')

print("===== HEAD DATA =====")
print(df.head())

print("\n===== INFO DATA =====")
print(df.info())

print("\n===== MISSING VALUE =====")
print(df.isnull().sum())

print("\n===== DESKRIPSI DATA =====")
print(df.describe())

plt.figure(figsize=(10,5))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.title('Visualisasi Missing Value')
plt.show()

df['Power_Level'] = pd.to_numeric(df['Power_Level'], errors='coerce')

top_power = df.sort_values(by='Power_Level', ascending=False).head(10)

plt.figure(figsize=(12,6))
sns.barplot(
    x='Character',
    y='Power_Level',
    data=top_power
)

plt.title('Top 10 Power Level Character')
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(8,5))

sns.countplot(
    x='Dragon_Ball_Series',
    data=df
)

plt.title('Jumlah Character per Series')
plt.show()

plt.figure(figsize=(12,6))

sns.countplot(
    y='Saga_or_Movie',
    data=df,
    order=df['Saga_or_Movie'].value_counts().index
)

plt.title('Jumlah Character per Saga')
plt.show()
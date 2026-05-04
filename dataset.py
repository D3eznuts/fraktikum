import pandas as pd
import matplotlib as plt
import seaborn as sns

df = pd.read_csv('./dataset/Dragon_Ball_Data_Set.csv')
print(df.head())
print(df.info())
print(df.isnull().sum())

df = df[df['Power_Level'] > 0]
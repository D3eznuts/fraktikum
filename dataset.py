import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv('./dataset/global_ecommerce_sales.csv', encoding='latin1')

# Rapihkan nama kolom
df.columns = (
    df.columns
    .str.strip()
    .str.replace(' ', '_')
)

print("===== KOLOM DATASET =====")
print(df.columns)

# =====================================
# CLEANING
# =====================================

# Convert tanggal
df['Order_Date'] = pd.to_datetime(
    df['Order_Date'],
    errors='coerce'
)

# Kolom numerik
numeric_cols = [
    'Discount_Percent',
    'Total_Sales',
    'Profit',
    'Shipping_Cost'
]

# Convert numerik
for col in numeric_cols:
    df[col] = pd.to_numeric(
        df[col],
        errors='coerce'
    )

# Hapus null
df = df.dropna(
    subset=[
        'Order_Date',
        'Discount_Percent',
        'Total_Sales'
    ]
)

print("\n===== INFO DATA =====")
print(df.info())

# =====================================
# 1. UNDERPERFORMER
# =====================================

plt.figure(figsize=(8,5))

plt.scatter(
    df['Discount_Percent'],
    df['Total_Sales']
)

plt.xlabel('Discount Percent')
plt.ylabel('Total Sales')
plt.title('Discount vs Total Sales')

plt.show()

underperform = df[
    (df['Discount_Percent'] > df['Discount_Percent'].mean()) &
    (df['Total_Sales'] < df['Total_Sales'].mean())
]

print("\n===== UNDERPERFORMER =====")
print(
    underperform[
        ['Discount_Percent', 'Total_Sales']
    ].head()
)

# =====================================
# 2. RFM ANALYSIS
# =====================================

snapshot_date = (
    df['Order_Date'].max()
    + dt.timedelta(days=1)
)

rfm = df.groupby('Customer_Name').agg({
    'Order_Date': lambda x:
        (snapshot_date - x.max()).days,

    'Order_ID': 'count',

    'Total_Sales': 'sum'
})

rfm.columns = [
    'Recency',
    'Frequency',
    'Monetary'
]

print("\n===== RFM =====")
print(rfm.head())

# =====================================
# 3. KONTRIBUSI NEGARA
# =====================================

country = (
    df.groupby('Country')['Total_Sales']
    .sum()
    .sort_values()
)

plt.figure(figsize=(10,6))

country.plot(kind='barh')

plt.title('Kontribusi Negara')
plt.xlabel('Total Sales')

plt.show()

# =====================================
# 4. UJI HIPOTESIS
# =====================================

median_disc = df['Discount_Percent'].median()

high = df[
    df['Discount_Percent'] > median_disc
]

low = df[
    df['Discount_Percent'] <= median_disc
]

print("\n===== HIPOTESIS =====")

print(
    "Rata-rata Sales Diskon Tinggi:",
    high['Total_Sales'].mean()
)

print(
    "Rata-rata Sales Diskon Rendah:",
    low['Total_Sales'].mean()
)

# =====================================
# 5. RFM SCORING
# =====================================

rfm['R_Score'] = pd.qcut(
    rfm['Recency'],
    5,
    labels=[5,4,3,2,1],
    duplicates='drop'
)

rfm['F_Score'] = pd.qcut(
    rfm['Frequency'].rank(method='first'),
    5,
    labels=[1,2,3,4,5],
    duplicates='drop'
)

rfm['M_Score'] = pd.qcut(
    rfm['Monetary'],
    5,
    labels=[1,2,3,4,5],
    duplicates='drop'
)

rfm['RFM_Group'] = (
    rfm['R_Score'].astype(str)
    + rfm['F_Score'].astype(str)
    + rfm['M_Score'].astype(str)
)

print("\n===== RFM SCORING =====")
print(rfm.head())

# =====================================
# 6. REGRESI LINEAR
# =====================================

X = df[['Discount_Percent']]
y = df['Total_Sales']

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LinearRegression()

model.fit(X_train, y_train)

print("\n===== REGRESI =====")

print(
    "Koefisien:",
    model.coef_[0]
)

print(
    "R2 Score:",
    model.score(X_test, y_test)
)

# =====================================
# HEATMAP
# =====================================

plt.figure(figsize=(8,6))

correlation = df[
    [
        'Total_Sales',
        'Discount_Percent',
        'Profit',
        'Shipping_Cost'
    ]
].corr()

sns.heatmap(
    correlation,
    annot=True,
    cmap='coolwarm'
)

plt.title('Korelasi Antar Variabel')

plt.show()
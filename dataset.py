import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# ================================
# LOAD DATA
# ================================
df = pd.read_csv('./dataset/global_ecommerce_sales.csv', encoding='latin1')
df.columns = df.columns.str.strip().str.replace(" ", "_")

print(df.columns)

df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')

# ================================
# 1. UNDERPERFORMER (ADAPTASI)
# ================================
# Pakai: Discount vs Total_Sales

plt.scatter(df['Discount_Percent'], df['Total_Sales'])
plt.xlabel('Discount')
plt.ylabel('Total Sales')
plt.title('Discount vs Sales')
plt.show()

underperform = df[
    (df['Discount_Percent'] > df['Discount_Percent'].mean()) &
    (df['Total_Sales'] < df['Total_Sales'].mean())
]

print("\n[1] Underperformer:")
print(underperform.head())

# ================================
# 2. RFM ANALYSIS
# ================================
snapshot_date = df['Order_Date'].max() + dt.timedelta(days=1)

rfm = df.groupby('Customer_Name').agg({
    'Order_Date': lambda x: (snapshot_date - x.max()).days,
    'Order_ID': 'count',
    'Total_Sales': 'sum'
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']

print("\n[2] RFM:")
print(rfm.head())

# ================================
# 3. KONTRIBUSI NEGARA (GANTI CATEGORY)
# ================================
country = df.groupby('Country')['Total_Sales'].sum().sort_values()

country.plot(kind='barh')
plt.title('Kontribusi Negara')
plt.show()

# ================================
# 4. UJI HIPOTESIS DISKON
# ================================
median_disc = df['Discount_Percent'].median()

high = df[df['Discount_Percent'] > median_disc]
low = df[df['Discount_Percent'] <= median_disc]

print("\n[4] Hipotesis:")
print("Diskon tinggi:", high['Total_Sales'].mean())
print("Diskon rendah:", low['Total_Sales'].mean())

# ================================
# 5. RFM SCORING
# ================================
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1], duplicates='drop')
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5], duplicates='drop')

rfm['RFM_Group'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

print("\n[5] RFM Scoring:")
print(rfm.head())

# ================================
# 6. REGRESI (DISKON → SALES)
# ================================
X = df[['Discount_Percent']]
y = df['Total_Sales']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)

print("\n[6] Regresi:")
print("Koefisien:", model.coef_[0])
print("R2 Score:", model.score(X_test, y_test))

# ================================
# HEATMAP TAMBAHAN
# ================================
sns.heatmap(df[['Total_Sales','Discount_Percent','Profit','Shipping_Cost']].corr(), annot=True)
plt.title('Korelasi')
plt.show()
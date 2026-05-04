# =========================
# 1. IMPORT LIBRARY
# =========================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

# =========================
# 2. LOAD DATA
# =========================
data = pd.read_csv('data_penjualan.csv')

print("Preview Data:")
print(data.head())

print("\nInfo Data:")
print(data.info())

print("\nMissing Value:")
print(data.isnull().sum())

# =========================
# 3. DATA CLEANING
# =========================
# ubah ke datetime
data['Order_Date'] = pd.to_datetime(data['Order_Date'])

# hapus harga negatif (kalau ada)
if 'Price' in data.columns:
    data = data[data['Price'] > 0]

# =========================
# 4. FEATURE ENGINEERING
# =========================
data['Year'] = data['Order_Date'].dt.year
data['Month'] = data['Order_Date'].dt.month

# =========================
# 5. ANALISIS TREND
# =========================
monthly_sales = data.groupby(['Year','Month'])['Sales'].sum().reset_index()
monthly_sales['YearMonth'] = monthly_sales['Year'].astype(str) + '-' + monthly_sales['Month'].astype(str)

plt.figure(figsize=(10,5))
plt.plot(monthly_sales['YearMonth'], monthly_sales['Sales'], marker='o')
plt.title('Tren Penjualan Bulanan')
plt.xticks(rotation=45)
plt.xlabel('Bulan')
plt.ylabel('Sales')
plt.show()

# =========================
# 6. KORELASI
# =========================
cols = ['Sales','Ad_Budget','Discount']
available = [c for c in cols if c in data.columns]

if len(available) > 1:
    corr = data[available].corr()
    sns.heatmap(corr, annot=True)
    plt.title('Heatmap Korelasi')
    plt.show()

# =========================
# 7. UNDERPERFORMER
# =========================
if 'Price' in data.columns and 'Quantity' in data.columns:
    plt.figure(figsize=(7,5))
    plt.scatter(data['Price'], data['Quantity'])
    plt.xlabel('Price')
    plt.ylabel('Quantity')
    plt.title('Produk Underperformer')
    plt.show()

# =========================
# 8. RFM ANALYSIS
# =========================
if 'CustomerID' in data.columns:
    snapshot_date = data['Order_Date'].max() + dt.timedelta(days=1)

    rfm = data.groupby('CustomerID').agg({
        'Order_Date': lambda x: (snapshot_date - x.max()).days,
        'Order_ID': 'count',
        'Sales': 'sum'
    })

    rfm.columns = ['Recency','Frequency','Monetary']

    # scoring
    rfm['R_Score'] = pd.qcut(rfm['Recency'],5,labels=[5,4,3,2,1])
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'),5,labels=[1,2,3,4,5])
    rfm['M_Score'] = pd.qcut(rfm['Monetary'],5,labels=[1,2,3,4,5])

    rfm['RFM_Group'] = rfm['R_Score'].astype(str)+rfm['F_Score'].astype(str)+rfm['M_Score'].astype(str)

    print("\nRFM Sample:")
    print(rfm.head())

# =========================
# 9. EFISIENSI KATEGORI
# =========================
if 'Category' in data.columns and 'Ad_Budget' in data.columns:
    cat = data.groupby('Category').agg({
        'Sales':'sum',
        'Ad_Budget':'sum'
    })

    cat['Efficiency'] = cat['Sales']/cat['Ad_Budget']
    cat = cat.sort_values('Efficiency')

    cat['Efficiency'].plot(kind='barh')
    plt.title('Efisiensi Kategori')
    plt.show()

# =========================
# 10. UJI HIPOTESIS
# =========================
if 'Ad_Budget' in data.columns:
    median_ads = data['Ad_Budget'].median()

    high = data[data['Ad_Budget'] > median_ads]
    low = data[data['Ad_Budget'] <= median_ads]

    print("\nRata-rata Sales Iklan Tinggi:", high['Sales'].mean())
    print("Rata-rata Sales Iklan Rendah:", low['Sales'].mean())
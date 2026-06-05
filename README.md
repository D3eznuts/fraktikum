# Proyek Analisis Dataset

Proyek ini berisi beberapa skrip Python untuk analisis dataset yang berbeda. Kami mengerjakan proyek ini bersama-sama, dengan pembagian tugas sebagai berikut:

- **dataset-jojo.py**: milik Dean Gavrilla
  - Dataset terkait: `dataset/jojostandstatsv2.csv`
- **dataset-dragon-ball.py**: milik Mahardika Arfuri
  - Dataset terkait: `dataset/Dragon_Ball_Data_Set.csv`
- **dataset-ecomerce.py** dan **dataset.py**: dikerjakan bersama
  - Dataset terkait: `dataset/global_ecommerce_sales.csv`

## Struktur Proyek

- `dataset-jojo.py`: analisis data JoJo Stand Stats, termasuk pemetaan ranking, visualisasi distribusi statistik, korelasi, dan daftar top 10 stand terkuat.
- `dataset-dragon-ball.py`: analisis data karakter Dragon Ball, termasuk pemeriksaan missing value, deskripsi data, visualisasi top power level, jumlah karakter per seri, dan jumlah karakter per saga.
- `dataset-ecomerce.py`: analisis awal data e-commerce, membersihkan data, dan menampilkan tren penjualan bulanan.
- `dataset.py`: analisis e-commerce yang lebih lengkap, termasuk pembersihan data, visualisasi, analisis underperformer, RFM, kontribusi negara, uji hipotesis diskon, dan scoring RFM.
- `dataset/`: folder berisi file CSV untuk masing-masing dataset.

## Dataset

- `dataset/jojostandstatsv2.csv`
- `dataset/Dragon_Ball_Data_Set.csv`
- `dataset/global_ecommerce_sales.csv`

## Persyaratan

Pastikan Anda memiliki Python dan paket berikut terpasang:

- pandas
- matplotlib
- seaborn
- scikit-learn (untuk `dataset.py`)

Anda dapat menginstalnya dengan:

```bash
pip install pandas matplotlib seaborn scikit-learn
```

## Cara Menjalankan

Jalankan setiap skrip dengan Python dari direktori proyek:

```bash
python dataset-jojo.py
python dataset-dragon-ball.py
python dataset-ecomerce.py
python dataset.py
```

## Catatan

- Semua dataset berada di folder `dataset/`.
- `dataset-jojo.py` dan `dataset-dragon-ball.py` masing-masing bertanggung jawab untuk analisis dataset mereka sendiri.
- `dataset-ecomerce.py` dan `dataset.py` adalah hasil kerja bersama kami.

Semoga README ini membantu menjelaskan pembagian tugas dan cara menggunakan skrip di proyek ini.
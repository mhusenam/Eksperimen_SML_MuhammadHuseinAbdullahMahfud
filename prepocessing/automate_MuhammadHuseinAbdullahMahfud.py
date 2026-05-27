import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def jalankan_otomatisasi(input_path, output_path):
    print(f"🔄 Memulai otomatisasi pra-pemrosesan...")
    print(f"📂 Membaca data mentah dari: {input_path}")
    
    # 1. Validasi cek apakah file mentah ada
    if not os.path.exists(input_path):
        print(f" Eror: File mentah di '{input_path}' tidak ditemukan!")
        return
        
    # 2. Membaca data asli
    df_raw = pd.read_csv(input_path)
    df_preprocessing = df_raw.copy()

    # 3. Membuat Kolom Target Utama (1 = Untung, 0 = Rugi)
    df_preprocessing['target'] = (df_preprocessing['profit'] > 0).astype(int)

    # 4. Ekstrak Fitur dari Tanggal
    df_preprocessing['order_date'] = pd.to_datetime(df_preprocessing['order_date'])
    df_preprocessing['order_month'] = df_preprocessing['order_date'].dt.month
    df_preprocessing['order_year'] = df_preprocessing['order_date'].dt.year

    # 5. Membuang kolom identitas dan kolom target asli agar tidak bocor
    kolom_tidak_dipakai = [
        'order_id', 'customer_id', 'customer_name', 'product_id', 
        'product_name', 'postal_code', 'profit', 'order_date', 'ship_date', 'target_visual'
    ]
    df_clean = df_preprocessing.drop(columns=kolom_tidak_dipakai, errors='ignore')

    # 6. Mengubah data teks kategorikal menjadi angka (Encoding)
    kolom_kategorikal = ['category', 'subcategory', 'ship_mode', 'segment', 'country', 'city', 'state', 'region']
    le = LabelEncoder()
    for col in kolom_kategorikal:
        df_clean[col] = le.fit_transform(df_clean[col])

    # 7. Membuat folder output secara otomatis jika belum ada
    folder_output = os.path.dirname(output_path)
    if folder_output and not os.path.exists(folder_output):
        os.makedirs(folder_output, exist_ok=True)

    # 8. Menyimpan hasil ke CSV baru
    df_clean.to_csv(output_path, index=False)
    print(f"🎉 Sukses! Data bersih berhasil disimpan di: {output_path}")
    print(f"📐 Ukuran data akhir: {df_clean.shape}")

if __name__ == "__main__":
    # Konfigurasi jalur file disesuaikan dengan struktur standar repositori kamu
    # Skrip ini dirancang untuk dijalankan dari root folder proyek
    PATH_INPUT = "namadataset_raw/superstore.csv"
    PATH_OUTPUT = "preprocessing/namadataset_preprocessing/superstore_preprocessing.csv"
    
    jalankan_otomatisasi(PATH_INPUT, PATH_OUTPUT)

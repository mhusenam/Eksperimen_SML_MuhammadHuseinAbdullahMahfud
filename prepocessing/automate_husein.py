import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def jalankan_otomatisasi(input_path, output_path):
    print(f"🔄 Memulai otomatisasi pra-pemrosesan...")
    print(f"📂 Membaca data mentah dari: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"❌ Eror: File mentah di '{input_path}' tidak ditemukan!")
        return
        
    # Menggunakan read_excel karena file aslimu berformat .xlsx
    df_raw = pd.read_excel(input_path)
    df_preprocessing = df_raw.copy()

    # Membuat Kolom Target Utama
    df_preprocessing['target'] = (df_preprocessing['profit'] > 0).astype(int)

    # Ekstrak Fitur dari Tanggal
    df_preprocessing['order_date'] = pd.to_datetime(df_preprocessing['order_date'])
    df_preprocessing['order_month'] = df_preprocessing['order_date'].dt.month
    df_preprocessing['order_year'] = df_preprocessing['order_date'].dt.year

    # Membuang kolom identitas
    kolom_tidak_dipakai = [
        'order_id', 'customer_id', 'customer_name', 'product_id', 
        'product_name', 'postal_code', 'profit', 'order_date', 'ship_date', 'target_visual'
    ]
    df_clean = df_preprocessing.drop(columns=kolom_tidak_dipakai, errors='ignore')

    # Mengubah data teks kategorikal menjadi angka
    kolom_kategorikal = ['category', 'subcategory', 'ship_mode', 'segment', 'country', 'city', 'state', 'region']
    le = LabelEncoder()
    for col in kolom_kategorikal:
        if col in df_clean.columns:
            df_clean[col] = le.fit_transform(df_clean[col].astype(str))

    # Menyimpan hasil ke CSV baru di folder preprocessing
    df_clean.to_csv(output_path, index=False)
    print(f"🎉 Sukses! Data bersih berhasil disimpan di: {output_path}")
    print(f"📐 Ukuran data akhir: {df_clean.shape}")

if __name__ == "__main__":
    # Jalur disesuaikan dengan letak file asli di GitHub kamu
    PATH_INPUT = "datasuperstore_raw.xlsx" 
    PATH_OUTPUT = "preprocessing/superstore_preprocessing.csv"
    
    jalankan_otomatisasi(PATH_INPUT, PATH_OUTPUT)
import pandas as pd
import numpy as np
from datetime import datetime

def clean_and_transform_data(raw_products: list) -> pd.DataFrame:
    """Membersihkan dan mengubah data produk mentah ke dalam bentuk DataFrame yang terstruktur."""

    if not raw_products:
        # Kembalikan DataFrame kosong jika tidak ada data
        return pd.DataFrame(columns=['title', 'price', 'rating', 'colors', 'size', 'gender', 'timestamp'])

    df = pd.DataFrame(raw_products)

    # Filter baris dengan judul tidak valid seperti "unknown"
    if 'title' in df.columns:
        df = df[~df['title'].str.lower().str.contains('unknown', na=False)]

    # Bersihkan dan konversi harga ke float dalam IDR
    df['price'] = df['price'].replace(r'[^\d.]', '', regex=True).replace('', np.nan)
    df.dropna(subset=['price'], inplace=True)
    df['price'] = df['price'].astype(float) * 16000  # Asumsi konversi 1 unit = 16.000 IDR

    # Bersihkan dan konversi rating ke float
    df['rating'] = df['rating'].replace(r'[^0-9.]', '', regex=True).replace('', np.nan)
    df.dropna(subset=['rating'], inplace=True)
    df['rating'] = df['rating'].astype(float)

    # Bersihkan dan ubah kolom rating menjadi float
    df['rating'] = df['rating'].replace(r'[^0-9.]', '', regex=True).replace('', np.nan)
    df.dropna(subset=['rating'], inplace=True)
    df['rating'] = df['rating'].astype(float).round(1)

    # Hilangkan label teks dari kolom size dan gender
    df['size'] = df['size'].replace(r'Size:\s*', '', regex=True)
    df['gender'] = df['gender'].replace(r'Gender:\s*', '', regex=True)

    # Hapus baris duplikat dan nilai kosong
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    # Tambahkan kolom waktu proses
    df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return df

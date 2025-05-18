import pandas as pd
from sqlalchemy import create_engine

def save_to_csv(dataframe: pd.DataFrame, filename="products.csv") -> None:
    """Menyimpan DataFrame ke file CSV lokal."""
    dataframe.to_csv(filename, index=False)
    print(f"Data berhasil disimpan ke file CSV: {filename}")

def save_to_postgresql(dataframe: pd.DataFrame, table_name='products') -> None:
    """Menyimpan DataFrame ke dalam tabel PostgreSQL."""

    try:
        # Konfigurasi koneksi ke database PostgreSQL
        db_username = 'postgres'
        db_password = 'Dp061203'
        db_host = 'localhost'
        db_port = '5432'
        db_name = 'product_db'

        # Buat koneksi ke PostgreSQL menggunakan SQLAlchemy
        engine = create_engine(f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')

        # Simpan DataFrame ke dalam tabel PostgreSQL (replace = timpa jika tabel sudah ada)
        dataframe.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data berhasil disimpan ke PostgreSQL, tabel: '{table_name}'")

    except Exception as error:
        print(f"Gagal menyimpan data ke PostgreSQL: {error}")

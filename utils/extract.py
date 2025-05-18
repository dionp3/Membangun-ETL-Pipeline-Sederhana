import requests
from bs4 import BeautifulSoup

def extract_data_from_page(url: str) -> list:
    """Mengambil data produk dari halaman koleksi berdasarkan URL."""

    try:
        # Kirim permintaan HTTP ke halaman
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        raise Exception(f"Gagal mengakses URL {url}: {error}")

    try:
        # Parsing isi halaman dengan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        extracted_products = []

        # Temukan semua elemen kartu produk
        cards = soup.find_all('div', class_='collection-card')
        if not cards:
            print(f"Tidak ada produk ditemukan di halaman {url}")

        for card in cards:
            # Ambil informasi produk dari elemen HTML
            title = card.find('h3', class_='product-title')
            price = card.find('div', class_='price-container')
            rating = card.find('p', string=lambda t: t and 'Rating' in t)
            colors = card.find('p', string=lambda t: t and 'Colors' in t)
            size = card.find('p', string=lambda t: t and 'Size' in t)
            gender = card.find('p', string=lambda t: t and 'Gender' in t)

            # Susun data ke dalam dictionary
            product = {
                'title': title.text.strip() if title else 'Unknown Title',
                'price': price.text.strip() if price else 'Price Not Available',
                'rating': rating.text.strip() if rating else 'No Rating',
                'colors': colors.text.strip() if colors else 'No Color Info',
                'size': size.text.strip() if size else 'No Size Info',
                'gender': gender.text.strip() if gender else 'No Gender Info',
            }

            extracted_products.append(product)

        print(f"{len(extracted_products)} produk berhasil diambil dari {url}")
        return extracted_products

    except Exception as parse_error:
        raise Exception(f"Terjadi kesalahan saat parsing HTML: {parse_error}")

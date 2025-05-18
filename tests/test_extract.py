import unittest
from unittest.mock import patch, Mock
from utils.extract import extract_data_from_page
from requests.exceptions import RequestException

class TestExtractData(unittest.TestCase):
    """Pengujian fungsi extract_data_from_page dari modul extract."""

    @patch('utils.extract.requests.get')
    def test_ekstraksi_berhasil(self, mock_get):
        """Mengujikan kasus ketika data berhasil diambil dari halaman HTML."""
        contoh_html = '''
        <div class="collection-card">
            <h3 class="product-title">Baju Keren</h3>
            <div class="price-container">100.00</div>
            <p>Rating: 4.5</p>
            <p>Colors: 3</p>
            <p>Size: L</p>
            <p>Gender: Male</p>
        </div>
        '''
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = contoh_html
        mock_get.return_value = mock_response

        hasil = extract_data_from_page("http://dummy-url")
        self.assertIsInstance(hasil, list)
        self.assertEqual(len(hasil), 1)
        self.assertEqual(hasil[0]['title'], 'Baju Keren')

    @patch('utils.extract.requests.get')
    def test_gagal_mengakses_url(self, mock_get):
        """Mengujikan kasus saat terjadi kegagalan koneksi saat mengambil data."""
        mock_get.side_effect = RequestException("Connection error")

        with self.assertRaises(Exception) as context:
            extract_data_from_page("http://dummy-url")

        self.assertIn('Gagal mengakses', str(context.exception))

    @patch('utils.extract.requests.get')
    def test_tidak_ada_produk_ditemukan(self, mock_get):
        """Mengujikan hasil ketika halaman tidak mengandung produk apa pun."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>No products here!</body></html>'
        mock_get.return_value = mock_response

        hasil = extract_data_from_page("http://dummy-url")
        self.assertIsInstance(hasil, list)
        self.assertEqual(len(hasil), 0)

if __name__ == '__main__':
    unittest.main()

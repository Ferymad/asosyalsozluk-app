import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from components.upload_component import upload_csv, display_upload_status
from io import StringIO

class TestUploadComponent(unittest.TestCase):
    def setUp(self):
        self.sample_csv = StringIO("""skor,baslik,entiri,silinmis,tarih
10,"Test Başlık","Test İçerik",False,2023-01-01 12:00:00
5,"Another Test","More Content",True,2023-01-02 13:00:00""")
    
    @patch('streamlit.file_uploader')
    @patch('services.csv_to_json.csv_to_json')
    def test_upload_csv(self, mock_csv_to_json, mock_file_uploader):
        mock_file_uploader.return_value = self.sample_csv
        mock_csv_to_json.return_value = [{"skor": 10, "baslik": "Test Başlık"}]
        
        result = upload_csv()
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['skor'], 10)
    
    @patch('streamlit.write')
    @patch('streamlit.json')
    def test_display_upload_status(self, mock_json, mock_write):
        json_data = [{"skor": 10, "baslik": "Test Başlık"}]
        display_upload_status(json_data)
        
        mock_write.assert_called_with("Number of entries: 1")
        mock_json.assert_called_with(json_data[0])
    
    @patch('streamlit.file_uploader')
    def test_upload_invalid_file(self, mock_file_uploader):
        mock_file_uploader.return_value = StringIO("invalid,csv,format")
        
        with self.assertRaises(KeyError):
            upload_csv()

if __name__ == '__main__':
    unittest.main()
    
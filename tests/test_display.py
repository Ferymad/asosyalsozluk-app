import unittest
from unittest.mock import patch
import json
from components.display_component import render_entry, sort_entries, filter_entries

class TestDisplayComponent(unittest.TestCase):
    def setUp(self):
        self.sample_entries = [
            {
                "skor": 10,
                "baslik": "Test Başlık",
                "entiri": "Test İçerik",
                "silinmis": False,
                "tarih": "2023-01-01 12:00:00"
            },
            {
                "skor": 5,
                "baslik": "Another Test",
                "entiri": "More Content",
                "silinmis": True,
                "tarih": "2023-01-02 13:00:00"
            }
        ]
    
    @patch('streamlit.markdown')
    def test_render_entry(self, mock_markdown):
        render_entry(self.sample_entries[0])
        mock_markdown.assert_called()
    
    def test_sort_entries(self):
        sorted_entries = sort_entries(self.sample_entries, 'skor', False)
        self.assertEqual(sorted_entries[0]['skor'], 10)
        self.assertEqual(sorted_entries[1]['skor'], 5)
        
        sorted_entries = sort_entries(self.sample_entries, 'baslik', True)
        self.assertEqual(sorted_entries[0]['baslik'], "Another Test")
        self.assertEqual(sorted_entries[1]['baslik'], "Test Başlık")
    
    def test_filter_entries(self):
        filtered = filter_entries(self.sample_entries, "Test", True)
        self.assertEqual(len(filtered), 2)
        
        filtered = filter_entries(self.sample_entries, "Another", False)
        self.assertEqual(len(filtered), 0)
        
        filtered = filter_entries(self.sample_entries, "Another", True)
        self.assertEqual(len(filtered), 1)

if __name__ == '__main__':
    unittest.main()
import unittest
import json
import pandas as pd
from services.csv_to_json import process_uploaded_file, csv_to_json

class TestCSVToJSON(unittest.TestCase):
    def setUp(self):
        self.sample_data = [
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
        
        self.df = pd.DataFrame(self.sample_data)
    
    def test_csv_to_json(self):
        result = csv_to_json(self.df)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['skor'], 10)
        self.assertEqual(result[1]['baslik'], "Another Test")
    
    def test_process_uploaded_file(self):
        # Create a temporary CSV file
        temp_csv = self.df.to_csv(index=False)
        result = process_uploaded_file(temp_csv)
        
        # Parse the JSON string result
        json_result = json.loads(result)
        
        self.assertIsInstance(json_result, list)
        self.assertEqual(len(json_result), 2)
        self.assertEqual(json_result[0]['skor'], 10)
        self.assertEqual(json_result[1]['silinmis'], True)
    
    def test_invalid_csv(self):
        invalid_df = pd.DataFrame({"invalid_column": [1, 2, 3]})
        with self.assertRaises(KeyError):
            csv_to_json(invalid_df)

if __name__ == '__main__':
    unittest.main()
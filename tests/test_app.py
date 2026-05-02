import unittest
import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from app import predict_house_price, app

class TestHousePricePredictor(unittest.TestCase):
    
    def test_predict_house_price_normal(self):
        """Test normal house price prediction"""
        price = predict_house_price(2000, 3, 5)
        expected = 50000 + (2000*300) + (3*15000) - (5*1000)
        self.assertEqual(price, expected)
    
    def test_predict_house_price_minimum(self):
        """Test minimum price constraint"""
        price = predict_house_price(0, 0, 100)
        self.assertGreaterEqual(price, 50000)
    
    def test_predict_house_price_large_area(self):
        """Test large area prediction"""
        price = predict_house_price(5000, 5, 10)
        self.assertGreater(price, 500000)
    
    def test_app_health_endpoint(self):
        """Test health check endpoint"""
        with app.test_client() as client:
            response = client.get('/health')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'healthy', response.data)
    
    def test_api_predict_endpoint(self):
        """Test REST API prediction endpoint"""
        with app.test_client() as client:
            response = client.post('/api/predict', 
                                 json={'area': 2000, 'bedrooms': 3, 'age': 5})
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertTrue(data['success'])
            expected = 50000 + (2000*300) + (3*15000) - (5*1000)
            self.assertEqual(data['prediction'], expected)

if __name__ == '__main__':
    unittest.main()

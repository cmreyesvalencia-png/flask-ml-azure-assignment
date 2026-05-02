from flask import Flask, request, jsonify, render_template_string
import numpy as np
import joblib
import os
import json

app = Flask(__name__)

# Simple house price prediction model
# Using a basic linear regression formula: price = base_price + (area * price_per_sqft) + (bedrooms * bedroom_value)
def predict_house_price(area, bedrooms, age):
    """
    Simple house price prediction function
    Formula: Price = 50000 + (area * 300) + (bedrooms * 15000) - (age * 1000)
    """
    base_price = 50000
    price_per_sqft = 300
    bedroom_value = 15000
    age_depreciation = 1000
    
    predicted_price = base_price + (area * price_per_sqft) + (bedrooms * bedroom_value) - (age * age_depreciation)
    
    # Ensure price is not negative
    return max(predicted_price, 50000)

# HTML template for the web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>House Price Predictor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background-color: #f0f0f0; }
        .container { max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; }
        input, button { width: 100%; padding: 10px; margin: 10px 0; }
        button { background-color: #007bff; color: white; border: none; cursor: pointer; }
        .result { margin-top: 20px; padding: 10px; background-color: #d4edda; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏠 House Price Predictor</h1>
        <form method="POST">
            <input type="number" name="area" placeholder="Area (sq ft)" required step="any">
            <input type="number" name="bedrooms" placeholder="Number of Bedrooms" required step="any">
            <input type="number" name="age" placeholder="Age of House (years)" required step="any">
            <button type="submit">Predict Price</button>
        </form>
        {% if prediction %}
        <div class="result">
            <h3>Predicted Price: ${{ "%.2f"|format(prediction) }}</h3>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        try:
            area = float(request.form['area'])
            bedrooms = float(request.form['bedrooms'])
            age = float(request.form['age'])
            prediction = predict_house_price(area, bedrooms, age)
        except Exception as e:
            prediction = f"Error: {str(e)}"
    return render_template_string(HTML_TEMPLATE, prediction=prediction)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """REST API endpoint for predictions"""
    try:
        data = request.get_json()
        area = float(data.get('area', 0))
        bedrooms = float(data.get('bedrooms', 0))
        age = float(data.get('age', 0))
        
        prediction = predict_house_price(area, bedrooms, age)
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'input': {'area': area, 'bedrooms': bedrooms, 'age': age}
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'house-price-predictor'})

# ==============================================
# NEW ENDPOINT ADDED FOR CI/CD VERIFICATION
# ==============================================
@app.route('/cd-status')
def cd_status():
    """Endpoint to verify CI/CD pipeline deployment"""
    return {
        'status': 'deployed',
        'pipeline': 'GitHub Actions CI/CD',
        'auto_deployment': 'enabled',
        'app_name': 'flask-houseprice-8580',
        'last_update': '2026-05-02',
        'version': '2.0'
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
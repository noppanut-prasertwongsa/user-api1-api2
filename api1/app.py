from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
import sys

app = Flask(__name__)
CORS(app)

# Configuration
API2_URL = os.getenv('API2_URL', 'http://api2:5000')

@app.route('/')
def home():
    """หน้าหลัก"""
    return jsonify({
        'service': 'API1',
        'message': 'Welcome to API1',
        'endpoints': ['/', '/call-api2', '/add-numbers']
    })

@app.route('/call-api2')
def call_api2():
    """เรียกใช้ API2 และรับคำตอบ hello world"""
    # --- บรรทัดสำหรับ Print Log ---
    print("============== START LOGGING ==============", file=sys.stdout)
    print("[API 1] request hello", file=sys.stdout)
    sys.stdout.flush() # <-- สั่งให้แสดง log ทันที
    # -----------------------------
    try:        
        response = requests.get(f"{API2_URL}/hello", timeout=10)
        response.raise_for_status()
        
        # --- บรรทัดสำหรับ Print Log ---
        print("============== END LOGGING ==============", file=sys.stdout)
        sys.stdout.flush()
        # -----------------------------

        return jsonify({
            'service': 'API1',
            'message': 'Successfully called API2',
            'response_from_api2': response.json()
        })
    except Exception as e:
        print(f'Error calling API2: {str(e)}')
        return jsonify({
            'service': 'API1',
            'error': 'Failed to call API2',
            'details': str(e)
        }), 500

@app.route('/add-numbers', methods=['GET', 'POST'])
def add_numbers():
    """ส่งตัวเลข 2 ตัวไปให้ API2 บวกกัน"""
    try:
        # รับค่าจาก query parameters หรือ request body
        if request.method == 'POST':
            data = request.json or {}
            num1 = data.get('num1', 10)
            num2 = data.get('num2', 20)
        else:
            num1 = int(request.args.get('num1', 10))
            num2 = int(request.args.get('num2', 20))
        
        # --- บรรทัดสำหรับ Print Log ---
        print("============== START LOGGING ==============", file=sys.stdout)
        print(f"[API 1] Received request to add numbers: num1={num1}, num2={num2}", file=sys.stdout) 
        print("[API 1] Forwarding request to API2...", file=sys.stdout)
        sys.stdout.flush()
        # -----------------------------
        
        # ส่งข้อมูลไปยัง API2
        payload = {'num1': num1, 'num2': num2}
        response = requests.post(
            f"{API2_URL}/calculate", 
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        response.raise_for_status()

        # --- บรรทัดสำหรับ Print Log ---
        print("[API 1] Successfully got response from API2.", file=sys.stdout)
        sys.stdout.flush()
        print("============== END LOGGING ==============", file=sys.stdout)
        sys.stdout.flush()
        # -----------------------------
        
        return jsonify({
            'service': 'API1',
            'message': 'Successfully calculated numbers with API2',
            'input': {'num1': num1, 'num2': num2},
            'response_from_api2': response.json()
        })
    except ValueError:
        return jsonify({
            'service': 'API1',
            'error': 'Invalid number format',
            'details': 'Please provide valid numbers'
        }), 400
    except Exception as e:
        print(f'Error calculating with API2: {str(e)}')
        return jsonify({
            'service': 'API1',
            'error': 'Failed to calculate with API2',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting API1 on port {port}")
    print(f"API2 URL: {API2_URL}")
    
    app.run(host='0.0.0.0', port=port, debug=True)
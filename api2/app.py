from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    """หน้าหลัก"""
    return jsonify({
        'service': 'API2',
        'message': 'Welcome to API2',
        'endpoints': ['/', '/hello', '/calculate']
    })

@app.route('/hello')
def hello_world():
    """ส่งคำตอบ hello world กลับไป"""
    # --- บรรทัดสำหรับ Print Log ---
    print("[API 2] Received request hello", file=sys.stdout)
    sys.stdout.flush()
    # -----------------------------
    return jsonify({
        'service': 'API2',
        'message': 'hello world'
    })

@app.route('/calculate', methods=['POST'])
def calculate():
    """รับตัวเลข 2 ตัว บวกกัน แล้วส่งผลลัพธ์กลับ"""
    try:
        data = request.json
        if not data:
            return jsonify({
                'service': 'API2',
                'error': 'No data provided'
            }), 400
        
        num1 = data.get('num1')
        num2 = data.get('num2')

        # --- บรรทัดสำหรับ Print Log ---
        print(f"[API 2] Received request to calculate: num1={num1}, num2={num2}", file=sys.stdout)
        sys.stdout.flush()
        # -----------------------------
        
        if num1 is None or num2 is None:
            return jsonify({
                'service': 'API2',
                'error': 'Missing num1 or num2',
                'required_format': {'num1': 'number', 'num2': 'number'}
            }), 400
        
        # แปลงเป็นตัวเลข
        num1 = float(num1)
        num2 = float(num2)
        
        # คำนวณผลลัพธ์
        result = num1 + num2
        
        # --- บรรทัดสำหรับ Print Log ---
        print(f"[API 2] Calculation result: {result}", file=sys.stdout)
        sys.stdout.flush()
        # -----------------------------

        
        return jsonify({
            'service': 'API2',
            'operation': 'addition',
            'input': {
                'num1': num1,
                'num2': num2
            },
            'result': result,
            'formula': f"{num1} + {num2} = {result}"
        })
        
    except (ValueError, TypeError) as e:
        return jsonify({
            'service': 'API2',
            'error': 'Invalid number format',
            'details': str(e)
        }), 400
    except Exception as e:
        print(f'Error in calculation: {str(e)}')
        return jsonify({
            'service': 'API2',
            'error': 'Calculation failed',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting API2 on port {port}")
    
    app.run(host='0.0.0.0', port=port, debug=True)
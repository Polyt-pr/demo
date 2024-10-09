from typing import Optional
import os
from functools import wraps
from dotenv import load_dotenv
from flask import jsonify, request

load_dotenv()

# authenticate internal requests
def internal(methods: Optional[list[str]] = None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not methods or request.method in methods:
                request_api_key = request.headers.get('X-API-Key')
                if not request_api_key or request_api_key != os.getenv('API_KEY'):
                    return jsonify({'error': 'Invalid API Key'}), 401
            return f(*args, **kwargs)
        return decorated_function
    return decorator
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.predict import predict

try:
    res = predict(25, 'Male', 170.0, 70.0, 'Moderate', 'No')
    print("Success:", res)
except Exception as e:
    import traceback
    traceback.print_exc()

"""
main.py — Entry point for model training.

Run this script FIRST before starting the Flask app:
    python main.py
"""

import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

from src.train import train

if __name__ == '__main__':
    print("=" * 60)
    print("  AI-Based Obesity Detection — Model Training")
    print("=" * 60)
    try:
        bundle, stats = train()
        print("\n" + "=" * 60)
        print("✅ Training complete!")
        print(f"   Ensemble Accuracy : {stats['ensemble']['accuracy'] * 100:.2f}%")
        print(f"   Ensemble F1 Score : {stats['ensemble']['f1'] * 100:.2f}%")
        print("=" * 60)
        print("\n🚀 You can now run the Flask app:")
        print("   python app.py")
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        raise

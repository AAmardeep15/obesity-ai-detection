"""
Download the UCI Obesity Levels dataset automatically.
Run: python download_dataset.py
"""
import urllib.request
import zipfile
import os
import shutil

DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

# UCI dataset direct download URL
URL = "https://archive.ics.uci.edu/static/public/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition.zip"

zip_path = os.path.join(DATA_DIR, 'obesity_dataset.zip')

print("⬇️  Downloading UCI Obesity Levels Dataset...")
try:
    urllib.request.urlretrieve(URL, zip_path)
    print("✅ Download complete.")

    print("📦 Extracting zip...")
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(DATA_DIR)

    # Find the CSV
    for root, dirs, files in os.walk(DATA_DIR):
        for f in files:
            if f.endswith('.csv'):
                src = os.path.join(root, f)
                dst = os.path.join(DATA_DIR, 'obesity_dataset.csv')
                shutil.copy(src, dst)
                print(f"✅ Dataset saved → {dst}")
                break

    # Clean up zip
    os.remove(zip_path)
    print("🎉 Done! You can now run: python main.py")

except Exception as e:
    print(f"❌ Download failed: {e}")
    print("\nManual steps:")
    print("1. Go to: https://archive.ics.uci.edu/dataset/544")
    print("2. Download the dataset ZIP")
    print("3. Extract and save the CSV as: data/obesity_dataset.csv")

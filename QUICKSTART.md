# Quick Start Guide

## Prerequisites
- Python 3.8+
- pip

## 3-Step Setup

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Add Dataset & Train Model
Download the UCI Obesity Dataset and save it as `data/obesity_dataset.csv`, then:
```bash
python main.py
```
Expected output:
```
✅ Dataset loaded: 2111 rows, 17 columns
🤖 Training individual models...
   Random Forest: Accuracy=0.9644 ...
   Logistic Regression: Accuracy=0.8793 ...
   Gradient Boosting: Accuracy=0.9549 ...
🗳️  Training Voting Ensemble...
   Ensemble: Accuracy=0.9573 ...
💾 Model saved → models/obesity_model.pkl
📊 Stats saved  → outputs/model_stats.json

✅ Training complete!
   Ensemble Accuracy : 95.73%
```

### Step 3 — Run the App
```bash
python app.py
```
Open: **http://localhost:5000**

## Dataset Download
- Source: [UCI ML Repository](https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition)
- File name: `ObesityDataSet_raw_and_data_sinthetic.csv`
- Save to: `data/obesity_dataset.csv`

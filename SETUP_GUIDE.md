# 🛠️ Detailed Setup & Execution Guide (Windows Focus)

Follow these steps to get your **Obesity Detection & Nutrition System** running from scratch.

---

## 1. Prerequisites
Ensure you have the following installed:
*   **Python 3.8 or higher** (Check by running: `python --version`)
*   **Git** (optional, for code management)

---

## 2. Environment Setup (Recommended)
Creating a Virtual Environment isolated this project's packages from your main system.

### Create the Environment
```powershell
python -m venv venv
```

### Activate the Environment
**On Windows (PowerShell):**
```powershell
.\venv\Scripts\activate
```
*(You will see `(venv)` appear on your terminal line.)*

**On Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

---

## 3. Install Dependencies
Once the environment is activated, install the required libraries:
```powershell
pip install -r requirements.txt
```

---

## 4. Prepare the Dataset
1. Create a folder named `data` in the project root if it doesn't exist.
2. Place your dataset file inside and rename it to: `obesity_dataset.csv`.
   *   *Full path should be: `data/obesity_dataset.csv`*

---

## 5. Train the Machine Learning Models
You must train the models once before the application can make predictions.
```powershell
python main.py
```
**What this does:**
*   Clean the data (Handling missing values/outliers).
*   Trains Random Forest, Logistic Regression, and Gradient Boosting.
*   Saves the final **Ensemble Model** to `models/obesity_model.pkl`.

---

## 6. Run the Web Application
Start the Flask development server:
```powershell
python app.py
```
**Access the App:**
*   Open your browser.
*   Go to: **`http://localhost:5000`**

---

## ⚠️ Troubleshooting (Windows Specific)

### 1. Execution Policy Error
If you cannot activate the `venv` because of a security error, run this in PowerShell as Administrator (or just in your current terminal):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

### 2. Missing "data" folder
If `main.py` fails saying it can't find the CSV, double-check that your file is named exactly `obesity_dataset.csv` and is inside the `data` folder.

### 3. Port already in use
If the app won't start because port 5000 is occupied, you can change the port in `app.py` or just close any other running python processes.

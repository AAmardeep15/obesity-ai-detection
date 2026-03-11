# 🤝 Team Setup & Virtual Environment Guide

If you are a teammate pulling this project for the first time, it is highly recommended to run this project inside a **Python Virtual Environment**. This ensures that the installed packages (`scikit-learn`, `flask`, etc.) don't conflict with other projects on your personal computer.

Follow these simple steps to get started:

---

## Step 1: Clone the Project
Make sure you have downloaded or cloned the project folder (`mini_pro`) and opened it in your terminal/command prompt.

```bash
cd mini_pro
```

---

## Step 2: Create the Virtual Environment
Run the following command to generate an isolated Python folder named `venv`.
```bash
# On Windows, Mac, and Linux:
python -m venv venv
```

---

## Step 3: Activate the Virtual Environment
You must activate the environment. You will know it worked if you see `(venv)` appear at the beginning of your terminal line.

**For Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**For Windows (PowerShell):**
```powershell
.\venv\Scripts\activate
```
*(Note: If PowerShell gives you a security error regarding execution policies, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` first, then try activating again.)*

**For macOS and Linux:**
```bash
source venv/bin/activate
```

---

## Step 4: Install the Required Packages
Now that your environment is safely active, install all the exact library versions needed for the AI model:

```bash
pip install -r requirements.txt
```

---

## Step 5: Run the Project!
You are fully set up. You can now train the model and start the web dashboard just like normal:

1. **Train the models (run this once):**
   ```bash
   python main.py
   ```

2. **Start the localized web app:**
   ```bash
   python app.py
   ```

3. Open your browser to **`http://localhost:5000`**

---
*To deactivate the virtual environment when you are done working, simply type `deactivate` in your terminal.*

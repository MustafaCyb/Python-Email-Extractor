
# 🚀 Python Email Extractor

A simple Python script for extracting emails from a specific URL and exporting the results into an HTML file.

---


## Setup

### 🛠️ Step 1: Create a Python Virtual Environment

Create a virtual environment to isolate your project dependencies.

- **Windows:**
  ```bash
  python -m venv myvenv
  ```

- **Linux:**
  ```bash
  python3 -m venv myvenv
  ```

- **macOS:**
  ```bash
  python3 -m venv myvenv
  ```

---

### 🌟 Step 2: Activate the Virtual Environment

Activate the virtual environment to begin using it.

- **Windows:**
  ```bash
  myvenv\Scripts\activate
  ```

- **Linux:**
  ```bash
  source myvenv/bin/activate
  ```

- **macOS:**
  ```bash
  source myvenv/bin/activate
  ```

---

### 📦 Step 3: Install Required Modules

Install the required Python modules from the `requirements.txt` file. Ensure your virtual environment is activated.

- **Windows:**
  ```bash
  pip install -r requirements.txt
  ```

- **Linux:**
  ```bash
  sudo pip install -r requirements.txt
  ```

- **macOS:**
  ```bash
  sudo pip install -r requirements.txt
  ```

> ⚠️ **Note**: For Linux/macOS, you may need to use `sudo` to avoid permission issues.

---

### ▶️ Step 4: Run the Script

Once the setup is complete, run your Python script.

- **Windows:**
  ```bash
  python email_extractor.py
  ```

- **Linux:**
  ```bash
  sudo python3 email_extractor.py
  ```

- **macOS:**
  ```bash
  sudo python3 email_extractor.py
  ```


---

### ⚠️ Notes:

- **Linux/macOS**: If you encounter permission issues while installing packages or running the script, prepend `sudo` to the command.
- **Windows**: During Python installation, make sure to add Python to your system's PATH.
- **Python Version**: On **Linux/macOS**, use `python3` if the default version is Python 2.x.

---
## 🛠️ Usage

This application features a simple **GUI** built using the `customtkinter` module.

---

### 🔤 Input Fields:
- **Target URL**:  
  Enter the target URL to search for emails.

- **Number of Threads**:  
  Specify the number of threads for the extraction operation.

- **Max URLs to Scan**:  
  Define the maximum number of URLs to be scanned, starting from the main URL, for email extraction.

- **Output HTML File**:  
  Provide the name of the generated HTML report. This file will contain the emails extracted from the scanned URLs.

---

### 🖱️ Buttons:
- **Start**:  
  Begins the email extraction process.

- **Stop**:  
  Halts the extraction process and saves the collected emails to the specified HTML file.

- **Clear Screen**:  
  Clears the logs and output from the extraction operation displayed in the GUI.

---

### ⚡ Notes:
- Ensure that the target URL is accessible.
- Use a reasonable number of threads (10-20 recommended) based on your system's capability for better performance.
- The output HTML report will be saved in the same directory as the executable/script unless otherwise specified.

---
## 📜 License:

This project is licensed under the **MIT License**. Feel free to modify or share it! 😊

---




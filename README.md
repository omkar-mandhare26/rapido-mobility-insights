
# Rapido Mobility Insights

## Project Objective
The objective of this project is to build a **Machine Learning–driven analytics and prediction system** that enables to:

* Predict ride outcomes before trip start
* Estimate fares accurately and dynamically
* Identify high-risk customers and unreliable drivers
* Support data-driven operational decisions

---
## Dataset

Download the dataset from the link below:

```
https://drive.google.com/drive/folders/1ZmESmEXCoVYzep1hXNagAE7wD3g-7uI1
```

### Dataset Placement

After downloading, place the dataset inside:

```
./dataset/
```

---

## Project Execution Flow

Follow the steps below **in order**.

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/omkar-mandhare26/rapido-mobility-insights.git
cd rapido-mobility-insights
```

---

### Step 2: Environment Setup

Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### Step 3: Run Notebooks (In Order)

Execute the notebooks in the following sequence:

```
1. data_preprocessing.ipynb
2. ride_outcome_model.ipynb
3. fare_prediction_model.ipynb
4. driver_delay_model.ipynb
5. customer_cancellation_risk_model.ipynb
```

Each notebook:

* Cleans / prepares data
* Trains and evaluates its respective model
* Saves artifacts for dashboard usage

---

### Step 4: Run the Streamlit Application

Launch the interactive dashboard:

```bash
streamlit run app.py
```

---

### Step 5: Access the Dashboard

Open in browser:

```
http://localhost:8501
```

---
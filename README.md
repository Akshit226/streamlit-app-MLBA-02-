# 💳 Credit Risk Assessment & Default Prediction Tool

> **Course:** Machine Learning for Business Applications (MLBA)  
> **Program:** MBA – Business Analytics  
> **Topic:** Banking & Financial Risk – Predicting Customer Loan Default  
> **Mode:** Team Project  

---

## 1. Project Title & Overview
**AI-Driven Credit Default Risk Analyzer:** An end-to-end machine learning decision support system deployed via Streamlit to evaluate loan applicants, quantify default risk, and provide actionable underwriting recommendations.

* **GitHub Repository:** https://github.com/Akshit226/streamlit-app-MLBA-02-
* **Live Deployed Application:** https://streamlit-app-mlba-02.streamlit.app (After Streamlit Cloud launch)

---

## 2. Business Problem Definition
Retail and commercial banks generate revenue by extending credit; however, borrower delinquency causes substantial **credit loss and accumulates Non-Performing Assets (NPAs)**. Traditional manual underwriting is slow and often subjective.

* **The Problem:** Lending institutions need a robust mechanism to identify borrowers at risk of default prior to capital disbursement.
* **The Asymmetric Cost of Errors:**
  * **False Negative (Costly):** Approving a borrower who defaults. The bank loses the principal loan amount.
  * **False Positive (Opportunity Cost):** Rejecting a creditworthy borrower. The bank loses interest margin and customer relationship.
  * **Strategic Focus:** The model is optimized for **Recall on Defaulters** to protect the bank's balance sheet.

---

## 3. Analytics Objective & Target Variable
* **Analytics Objective:** Train a supervised binary classification model that accurately predicts the likelihood of borrower default and deploys as an interactive web tool for loan officers.
* **Target Variable:** `class`
  * `bad` (1) = High Risk / Defaulter
  * `good` (0) = Low Risk / Non-defaulter

---

## 4. Dataset Information
* **Dataset Name:** Statlog German Credit Data
* **Source:** UCI Machine Learning Repository / OpenML
* **Observations:** 1,000 historic credit applicants
* **Features:** 20 predictor attributes (financial history, current liquidity, demographics, loan parameters)
* **Class Distribution:** 700 Good (70%) vs. 300 Bad (30%)

---

## 5. End-to-End Methodology
```
Raw Data (German Credit) 
  ↓
Data Cleaning & Feature Encoding
  ↓
Exploratory Data Analysis (EDA & Insights)
  ↓
Stratified Train/Test Split (80/20)
  ↓
Model Training (Random Forest with Balanced Class Weights)
  ↓
Evaluation (Accuracy, Precision, Recall, F1, Confusion Matrix)
  ↓
Model Serialization (`model.pkl` via joblib)
  ↓
Interactive 3-Page Streamlit App (`app.py`)
  ↓
Cloud Deployment (Streamlit Community Cloud)
```

---

## 6. Model Architecture & Performance
* **Algorithm Selected:** `Random Forest Classifier` (`n_estimators=100`, `max_depth=6`, `class_weight='balanced'`)
* **Preprocessing:** `ColumnTransformer` with `StandardScaler` for numerical attributes and `OneHotEncoder` for categorical categories wrapped in a Scikit-Learn `Pipeline`.

### Test Performance Metrics (20% Holdout)
| Metric | Score | Business Rationale |
| :--- | :--- | :--- |
| **Accuracy** | **70.0%** | Baseline accuracy across the balanced test holdout. |
| **Recall (Defaulters)** | **71.7%** | Successfully catches ~72% of high-risk defaulters. |
| **Precision (Defaulters)** | **50.0%** | Half of all flagged applicants are true defaults. |
| **F1-Score** | **0.589** | Harmonic mean balancing recall and precision. |

---

## 7. Key Business Insights (EDA)
1. **Checking Account Balance is the #1 Signal:** Applicants with negative checking balances (`< 0 DM`) experience default rates approaching **50%**, whereas those with $\ge 200\text{ DM}$ default under **15%**.
2. **Tenure Multiplies Exposure:** Median loan duration for defaulters is **30 months**, compared to **18 months** for repayers. Longer horizons introduce financial uncertainty.
3. **Liquidity Matters:** Having savings $\ge 1,000\text{ DM}$ acts as a significant safety net against unexpected personal liquidity shocks.

---

## 8. Repository Structure
```
business-analytics-project/
├── app.py                          # 3-Page Streamlit Web Application
├── model.pkl                       # Trained serialized Scikit-Learn pipeline
├── requirements.txt                # Python environment dependencies
├── README.md                       # Comprehensive project documentation
├── data/
│   └── german_credit_data.csv      # Raw dataset (1,000 records)
├── notebooks/
│   └── model_development.ipynb    # Step-by-step Jupyter Notebook
└── images/
    ├── fig1_risk_distribution.png
    ├── fig2_checking_vs_default.png
    ├── fig3_duration_vs_risk.png
    └── fig4_credit_amount_vs_age.png
```

---

## 9. How to Run the Application Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/business-analytics-project.git
   cd business-analytics-project
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Streamlit web app:**
   ```bash
   streamlit run app.py
   ```
   The interactive app will launch automatically in your web browser at `http://localhost:8501`.

---

## 10. Cloud Deployment Guide (Streamlit Community Cloud)
1. Push this directory to your personal or team GitHub repository.
2. Visit [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
3. Click **"New App"** $\rightarrow$ Select your repository, branch (`main`), and set Main file path to `app.py`.
4. Click **"Deploy"**. Your live decision tool will be accessible worldwide in ~2 minutes!

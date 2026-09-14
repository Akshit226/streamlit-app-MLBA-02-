# 💳 MLBA Assignment 2: End-to-End Project Walkthrough & Explanation Guide
> **Course:** Machine Learning for Business Applications (MLBA) — MBA Business Analytics  
> **Topic:** AI-Driven Credit Risk Assessment & Loan Default Decision Support System  
> **Written In:** Simple, non-technical plain English with MBA-level business context  

---

## 📌 1. The Big Picture: What Was This Assignment About?

Imagine you are hired as a **Business Analyst at a retail bank**. 

Every single day, hundreds of customers walk in or apply online for personal and car loans. 
* If the bank is **too strict** and rejects everyone, it makes zero revenue and loses customers to competitors.
* If the bank is **too reckless** and gives loans to anyone, borrowers stop paying, loans turn into **Non-Performing Assets (NPAs)**, and the bank loses millions in capital.

### The Assignment Goal:
Your professor tasked you with building a **complete, end-to-end data-driven decision tool**:
1. Take historical loan data from past applicants.
2. Teach a machine learning algorithm to recognize patterns of who defaults and who repays.
3. Package that model into a clean, interactive 3-page web application using **Streamlit**.
4. Push everything to **GitHub** and deploy it live on the internet so loan officers (and faculty) can use it in a web browser.
5. Provide clear **business recommendations**, not just raw mathematical numbers.

---

## 🏛️ 2. Step 1: Choosing the Business Problem & The Asymmetric Cost Rule

Before writing a single line of code, the assignment required choosing a problem where machine learning directly impacts a business decision.

We selected: **Banking Credit Risk Underwriting (Loan Default Prediction)**.

### Why This Problem? The "Asymmetric Cost" of Mistakes:
In standard machine learning, people often assume that making a mistake in one direction is the same as making a mistake in the other. In banking, that is completely false!

Consider the two mistakes a model can make:
1. **Mistake A (False Positive - Turning away a good customer):**
   * *What happens:* The applicant was honest and would have repaid, but the model flagged them as risky.
   * *Business Cost:* **Low/Moderate.** The bank loses the interest margin (e.g., 8–10% interest profit). The applicant might go to another bank.
2. **Mistake B (False Negative - Approving a borrower who defaults):**
   * *What happens:* The model said the borrower was safe, the bank lent \$10,000, and the borrower disappeared.
   * *Business Cost:* **Severe / Critical.** The bank loses 100% of the principal loan amount plus collection/legal expenses.

> **Key Rule for the Project:**  
> Missing a defaulter (Mistake B) is **10 to 15 times more dangerous** to a bank than accidentally rejecting a good borrower (Mistake A). Therefore, our entire project was designed to maximize **Recall on Defaulters** (catching as many bad loans as possible).

---

## 📂 3. Step 2: The Dataset (Statlog German Credit Data)

We obtained the benchmark **German Credit Dataset** (from the UCI Machine Learning Repository / OpenML):
* **Total Observations:** 1,000 historical bank loan applicants.
* **The Target Variable (`class`):**
  * `good` (0): 700 applicants (70%) — repaid their loan satisfactorily.
  * `bad` (1): 300 applicants (30%) — defaulted or experienced major payment delinquency.
* **Features Available:** 20 predictor attributes covering:
  * Financial stability (checking account balance, savings account balance).
  * Repayment history (existing credits, delayed payments in the past).
  * Loan characteristics (duration in months, amount requested, purpose).
  * Demographic/Personal stability (age, employment tenure, housing status).

---

## 🧹 4. Step 3: Data Cleaning & Feature Preparation

In real-world business analytics, feeding 20 complex, messy features into a tool confuses loan officers. We selected the **8 most powerful and practical features** that any loan officer can collect in 2 minutes:

| Feature Name | Type | Real-World Business Meaning |
| :--- | :--- | :--- |
| `checking_status` | Categorical | How much liquid cash the applicant has in their daily checking account (`<0 DM`, `0-200 DM`, `>=200 DM`, or `no checking account`). |
| `duration` | Numerical | How many months the borrower wants the loan for (e.g., 12, 24, 48 months). |
| `credit_amount` | Numerical | Total money requested (in DM / currency units). |
| `savings_status` | Categorical | Total rainy-day emergency fund / savings buffer (`<100 DM`, `100-500 DM`, etc.). |
| `employment` | Categorical | Job stability (unemployed, `<1 yr`, `1-4 yrs`, `4-7 yrs`, `>=7 yrs`). |
| `age` | Numerical | Age of the borrower in years. |
| `housing` | Categorical | Whether they own their house, rent, or live for free. |
| `purpose` | Categorical | Why they need the loan (radio/tv, new car, used car, business, education, etc.). |

### Preparing the Data for the Algorithm:
1. **Target Encoding:** We converted `class` into numbers: `bad = 1` (positive class / defaulter) and `good = 0` (negative class / non-defaulter).
2. **Train / Test Split (80/20):**
   * We held back **20% (200 applicants)** in a test vault that the model was never allowed to see during training.
   * We used **stratified splitting** so both train and test sets had exactly 30% defaulters and 70% repayers.
3. **Column Transformer Pipeline:**
   * **Numerical scaling (`StandardScaler`):** Normalizes duration, loan amount, and age so large numbers (like \$10,000 loan) don't overpower smaller numbers (like 24 months).
   * **Categorical encoding (`OneHotEncoder`):** Converts categories like "own house" vs "rent" into binary 1s and 0s.

---

## 🔍 5. Step 4: Exploratory Data Analysis (EDA) — Key Business Findings

When we explored the historical data using charts, three clear patterns emerged:

1. **Insight 1: Checking Account Liquidity is the #1 Early Warning Signal**
   * Applicants with negative checking balances (`< 0 DM`) had a default rate close to **50%**!
   * Applicants with healthy reserves ($\ge 200\text{ DM}$) had default rates under **15%**.
   * *Business Takeaway:* Liquid cash is the primary buffer against immediate default.

2. **Insight 2: Loan Duration Multiplies Risk**
   * Borrowers who defaulted had a median loan duration of **30 months**, compared to only **18 months** for those who repaid.
   * *Business Takeaway:* The longer the loan term, the more time there is for life events (job loss, illness, divorce) to derail repayment.

3. **Insight 3: Savings Buffers Prevent Default**
   * Borrowers with savings above $1,000\text{ DM}$ rarely defaulted, even when borrowing larger amounts.

---

## 🤖 6. Step 5: Choosing and Training the Machine Learning Model

We chose **Random Forest Classifier**.

### Why Random Forest in Simple Language?
A single Decision Tree is like asking **one** junior loan officer for their opinion. They might have personal biases or make mistakes on edge cases.

A **Random Forest** creates an entire committee of **100 independent loan officers (100 trees)**. Each officer looks at different combinations of applicant features and votes. The final decision is the average consensus of all 100 trees. This makes the predictions much more stable and accurate.

### The Critical Hyperparameter: `class_weight='balanced'`
Because only 30% of the applicants were defaulters, a standard model might get lazy and mostly predict "Good".
By turning on `class_weight='balanced'`, we told the algorithm:
> *"Every time you fail to catch a defaulter, penalize yourself heavily! Treat finding defaulters as top priority."*

---

## 📈 7. Step 6: Model Evaluation & The Confusion Matrix Explained

When we tested our model on the **200 unseen holdout applicants** (140 Good borrowers, 60 Bad borrowers), here were the exact results:

### The Confusion Matrix:
| | Predicted: Low Risk (Good) | Predicted: High Risk (Bad) | Total Actual |
| :--- | :---: | :---: | :---: |
| **Actual Low Risk (Good)** | **97** (True Negatives) | **43** (False Positives) | 140 |
| **Actual High Risk (Defaulters)** | **17** (False Negatives) | **43** (True Positives) | 60 |

### Translating the Metrics to Executive Terms:
* **Recall on Defaulters = 71.7% (`43 / 60`):**
  * The model caught **almost 72% of all potential defaulters** before they received money.
  * Only 17 bad loans slipped through.
* **Accuracy = 70.0% (`(97 + 43) / 200`):**
  * Across all applicants, 7 out of 10 predictions were spot on.
* **Precision = 50.0% (`43 / (43 + 43)`):**
  * When the model raises a red flag, half of those flagged are true defaulters, and half are borderline good applicants. 
  * *Business Action:* That's why flagged applicants are sent for **secondary manual underwriting** (requesting collateral or a co-signer) rather than getting automatically rejected.

---

## 💾 8. Step 7: Saving the Model (`model.pkl`)

In professional software development, you never retrain a model inside a user-facing website.
* Training takes time, memory, and raw training data.
* Instead, we used Python's `joblib.dump(pipeline, "model.pkl")` to freeze the entire pipeline (scalers + encoders + 100 decision trees) into a single compact file: `model.pkl`.
* When the web application starts, it loads `model.pkl` in **0.1 seconds** and is ready to make predictions instantly.

---

## 💻 9. Step 8: Creating the 3-Page Streamlit App (`app.py`)

Using Streamlit, we built an interactive dashboard structured into three pages:

```
Streamlit Decision Tool
├── Page 1: Business Problem & Context (Explains the banking challenge & dataset)
├── Page 2: Data Insights & EDA (Interactive charts on checking status, duration, risk)
└── Page 3: Credit Risk Predictor (Live underwriting engine for loan officers)
```

### How Page 3 (The Predictor) Works in Real Life:
1. The loan officer enters the borrower's details (e.g., 24 months, \$3,500 loan amount, checking balance `< 0 DM`, job duration 3 years).
2. The officer clicks **"Assess Credit Risk"**.
3. The app feeds the inputs into `model.pkl` and calculates the **Default Probability (0% to 100%)**.
4. The app maps this probability into three business tiers:
   * **Green Tier ($P < 40\%$): Low Risk / Approved.** Fast-track straight-through processing.
   * **Yellow Tier ($40\% \le P \le 60\%$): Moderate Risk / Manual Review.** Request collateral, co-signer, or proof of supplementary income.
   * **Red Tier ($P > 60\%$): High Risk / Decline.** High risk of capital loss; decline or restructure loan tenure.

---

## 🐙 10. Step 9: Git, GitHub & Project Structure

The project was structured cleanly following industry standards:

```
business-analytics-project/
├── app.py                          # The 3-page Streamlit web application
├── model.pkl                       # Trained Random Forest pipeline
├── requirements.txt                # List of Python dependencies
├── README.md                       # Comprehensive rubric-aligned report
├── .gitignore                      # Keeps junk/cache files out of git
├── data/
│   └── german_credit_data.csv      # 1,000 applicant dataset
├── notebooks/
│   └── model_development.ipynb    # Training & evaluation Jupyter notebook
└── images/                         # Exported figures used in Streamlit and README
    ├── fig1_risk_distribution.png
    ├── fig2_checking_vs_default.png
    ├── fig3_duration_vs_risk.png
    └── fig4_credit_amount_vs_age.png
```

* **GitHub Repository:** [https://github.com/Akshit226/streamlit-app-MLBA-02-](https://github.com/Akshit226/streamlit-app-MLBA-02-)
* We maintained a clean commit history and added `.gitignore` so Python cache folders (`__pycache__`) do not pollute the repository.

---

## ☁️ 11. Step 10: Cloud Deployment (Streamlit Community Cloud)

To make the app accessible to anyone on the internet without needing Python installed on their computer:
1. The code is synced to GitHub.
2. Streamlit Community Cloud links to `Akshit226/streamlit-app-MLBA-02-`.
3. When launched, Streamlit spins up a cloud server, automatically installs everything listed in `requirements.txt`, executes `app.py`, and gives you a public URL (`https://akshit226-streamlit-app-mlba-02--app-hemxe8.streamlit.app/`).

---

## 🎯 12. Summary for Your Viva / Presentation

If your professor asks: *"In one minute, what did your team accomplish in this project?"*

> **Your Elevator Pitch:**  
> *"We built an end-to-end AI-driven credit underwriting decision tool for retail lending using the German Credit dataset. Rather than just maximizing generic accuracy, we designed our Random Forest model around the asymmetric cost of banking defaults, optimizing for Recall so we catch 71.7% of high-risk borrowers. We packaged the entire pipeline into a serialized model and deployed a 3-page Streamlit web tool where loan officers can input applicant details and receive instant risk scores, triage tiers, and underwriting recommendations."*

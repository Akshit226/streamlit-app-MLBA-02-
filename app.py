import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Credit Risk Decision Tool",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .sub-header { font-size: 16px; color: #4B5563; margin-bottom: 20px; }
    .card { background-color: #F8FAFC; border-radius: 10px; padding: 20px; border: 1px solid #E2E8F0; margin-bottom: 15px; }
    .metric-value { font-size: 24px; font-weight: bold; color: #0F172A; }
    </style>
""", unsafe_allow_html=True)

# Helper function to load model safely
@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    if not os.path.exists(model_path):
        st.error(f"Model file not found at {model_path}. Please ensure model.pkl exists.")
        return None
    return joblib.load(model_path)

model = load_model()

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/fluency/96/bank-building.png", width=70)
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["1. Business Problem", "2. Data Insights (EDA)", "3. Credit Risk Predictor"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Course:** MLBA - MBA Business Analytics  
**Project:** German Credit Risk Assessment  
**Model:** Random Forest Classifier  
""")

# ==========================================
# PAGE 1: BUSINESS PROBLEM & CONTEXT
# ==========================================
if page == "1. Business Problem":
    st.markdown('<div class="main-header">💳 Credit Risk Assessment & Default Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Decision Support Tool for Retail Lending</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("1. Business Background")
        st.write("""
        Commercial banks and credit institutions operate on interest income derived from issued loans. 
        However, when borrowers fail to repay obligations, institutions face severe credit risk, 
        accumulating **Non-Performing Assets (NPAs)** and losing their loan principals.
        
        Historically, credit analysts relied on manual underwriting rules which are either too slow 
        or prone to human bias and inconsistent decisions.
        """)
        
        st.subheader("2. The Analytics Objective")
        st.write("""
        The objective is to deploy a machine learning decision tool that:
        * **Predicts borrower default risk** before disbursing funds.
        * **Quantifies default probability** to distinguish safe, borderline, and high-risk applicants.
        * **Generates prescriptive business recommendations** (Approve, Conditionally Approve, or Reject).
        """)
        
        st.subheader("3. Decision Framework & Economic Trade-offs")
        st.write("""
        In credit risk evaluation, errors have asymmetric business costs:
        * **False Negative (Costly):** The model predicts an applicant is 'Good', but they default. The bank loses the principal loan amount.
        * **False Positive (Opportunity Cost):** The model flags a creditworthy customer as 'High Risk'. The bank loses interest margin and customer goodwill.
        
        Therefore, our model is calibrated to maximize **Recall on Defaulters** while keeping false rejections reasonable.
        """)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Dataset Summary")
        st.markdown("**Source:** German Credit (UCI Machine Learning Repository / OpenML)")
        st.markdown("**Observations:** 1,000 loan applicants")
        st.markdown("**Target Variable:** `class` (Good vs Bad Risk)")
        st.markdown("**Class Balance:** 700 Good (70%) | 300 Bad (30%)")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Decision Policy")
        st.markdown("🟢 **< 35% Risk:** Approve loan at standard rates.")
        st.markdown("🟡 **35% – 55% Risk:** Conditional approval (shorter term / guarantor required).")
        st.markdown("🔴 **> 55% Risk:** Reject or mandate full collateral backing.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PAGE 2: DATA INSIGHTS (EDA)
# ==========================================
elif page == "2. Data Insights (EDA)":
    st.markdown('<div class="main-header">📈 Exploratory Data Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Key empirical drivers of credit default extracted from historical data</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Checking Balance Impact", "Loan Tenure & Risk", "Overall Portfolio Distribution"])
    
    base_img_path = os.path.join(os.path.dirname(__file__), "images")
    
    with tab1:
        st.subheader("Checking Account Balance: The Strongest Solvency Signal")
        col_img, col_desc = st.columns([1.2, 1])
        with col_img:
            img_path = os.path.join(base_img_path, "fig2_checking_vs_default.png")
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.warning("Figure not found at path.")
        with col_desc:
            st.markdown("""
            #### **Managerial Takeaway:**
            * Applicants with **negative checking balances (`< 0 DM`)** exhibit a default rate approaching **50%**.
            * Applicants with no active checking account or balances $\\ge$ 200 DM have default rates under **15%**.
            * **Policy Action:** Applicants with negative checking accounts must not be offered unsecured personal loans without verified liquid assets.
            """)
            
    with tab2:
        st.subheader("Loan Duration vs. Default Rate")
        col_img, col_desc = st.columns([1.2, 1])
        with col_img:
            img_path = os.path.join(base_img_path, "fig3_duration_vs_risk.png")
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.warning("Figure not found at path.")
        with col_desc:
            st.markdown("""
            #### **Managerial Takeaway:**
            * The median loan duration for defaulting loans is **significantly longer (~30 months)** compared to performing loans (~18 months).
            * Over extended time horizons, personal financial shocks (job loss, illness) accumulate, multiplying default probabilities.
            * **Policy Action:** For borderline applicants, counteroffer with a shorter repayment horizon (e.g. 12–18 months).
            """)

    with tab3:
        st.subheader("Credit Risk Breakdown across 1,000 Historic Applicants")
        col_img, col_desc = st.columns([1.2, 1])
        with col_img:
            img_path = os.path.join(base_img_path, "fig1_risk_distribution.png")
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.warning("Figure not found at path.")
        with col_desc:
            st.markdown("""
            #### **Portfolio Composition:**
            * **700 Good (70%) vs. 300 Bad (30%)**.
            * Class imbalance requires **balanced penalty weights** during model training so the classifier does not blindly favour the majority class.
            """)

# ==========================================
# PAGE 3: PREDICTION TOOL
# ==========================================
elif page == "3. Credit Risk Predictor":
    st.markdown('<div class="main-header">🧮 Interactive Credit Risk Evaluation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Enter applicant details below to generate instant credit assessment and recommendation</div>', unsafe_allow_html=True)
    
    with st.form("applicant_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("##### 🏦 Financial Standing")
            checking_status = st.selectbox(
                "Checking Account Balance",
                options=["<0", "0<=X<200", ">=200", "no checking"],
                index=1,
                help="Existing balance in current account"
            )
            savings_status = st.selectbox(
                "Savings Account Balance",
                options=["<100", "100<=X<500", "500<=X<1000", ">=1000", "no known savings"],
                index=0,
                help="Total liquid savings available"
            )
            
        with col2:
            st.markdown("##### 📄 Loan Request")
            credit_amount = st.slider(
                "Credit Amount (in DM)",
                min_value=250, max_value=20000, value=2500, step=250,
                help="Total requested loan principal"
            )
            duration = st.slider(
                "Loan Duration (in Months)",
                min_value=4, max_value=72, value=24, step=2,
                help="Tenure of the repayment period"
            )
            purpose = st.selectbox(
                "Loan Purpose",
                options=["radio/tv", "new car", "used car", "furniture/equipment", "business", "education", "repairs", "other"],
                index=0
            )

        with col3:
            st.markdown("##### 👤 Demographics & Stability")
            age = st.slider(
                "Applicant Age (Years)",
                min_value=18, max_value=75, value=32
            )
            employment = st.selectbox(
                "Employment Duration",
                options=["<1", "1<=X<4", "4<=X<7", ">=7", "unemployed"],
                index=1,
                help="Years at current employer"
            )
            housing = st.selectbox(
                "Housing Situation",
                options=["own", "rent", "for free"],
                index=0
            )
            
        submitted = st.form_submit_button("⚡ Assess Credit Risk", use_container_width=True)

    if submitted:
        if model is None:
            st.error("Model is not loaded. Please ensure model.pkl is trained and present.")
        else:
            input_df = pd.DataFrame([{
                'checking_status': checking_status,
                'duration': duration,
                'credit_amount': credit_amount,
                'savings_status': savings_status,
                'employment': employment,
                'age': age,
                'housing': housing,
                'purpose': purpose
            }])
            
            # Predict default probability
            prob_default = model.predict_proba(input_df)[0][1]
            prob_good = 1 - prob_default
            
            st.markdown("---")
            st.subheader("📋 Decision Output & Risk Profile")
            
            res_col1, res_col2 = st.columns([1, 1])
            
            with res_col1:
                delta_sign = "-" if prob_default < 0.4 else "+"
                st.metric(
                    label="Estimated Default Probability",
                    value=f"{prob_default:.1%}",
                    delta=f"{delta_sign} Risk Score",
                    delta_color="inverse"
                )
                st.progress(float(prob_default))
                
                if prob_default < 0.35:
                    st.success("### ✅ Recommendation: APPROVE")
                    st.write("**Action Plan:** Disburse requested principal at standard prime interest rate. No additional collateral required.")
                elif prob_default <= 0.55:
                    st.warning("### ⚠️ Recommendation: CONDITIONAL APPROVAL")
                    st.write("**Action Plan:** High sensitivity zone. Counteroffer with a lower loan principal or shorten tenure to under 18 months, or mandate a creditworthy co-signer.")
                else:
                    st.error("### ❌ Recommendation: REJECT / ESCALATE")
                    st.write("**Action Plan:** Probability of delinquency exceeds portfolio threshold. Decline application or require 100% asset-backed collateral.")

            with res_col2:
                st.markdown("#### 🎯 Risk Score Breakdown")
                fig, ax = plt.subplots(figsize=(5, 2.5))
                categories = ['Repayment Probability', 'Default Risk']
                scores = [prob_good * 100, prob_default * 100]
                colors = ['#2ECC71', '#E74C3C']
                
                bars = ax.barh(categories, scores, color=colors, height=0.55)
                ax.set_xlim(0, 100)
                ax.set_xlabel('Probability (%)')
                for bar in bars:
                    width = bar.get_width()
                    ax.text(width + 2, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', va='center', fontweight='bold')
                
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                st.pyplot(fig)
                plt.close(fig)

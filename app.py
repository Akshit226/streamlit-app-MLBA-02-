import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import datetime

# ==============================================================================
# 1. PAGE CONFIGURATION & HIGH-LEGIBILITY DESIGN SYSTEM
# ==============================================================================
st.set_page_config(
    page_title="Credit Risk Decision Tool | MLBA",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, High-Readability Consulting Typography & Universal Contrast CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global Typography - Large, Crisp, High Contrast */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 16px;
        line-height: 1.6;
        color: #0F172A;
    }

    /* Titles and Section Headers */
    .mck-header {
        font-size: 30px;
        font-weight: 800;
        color: #00205B;
        letter-spacing: -0.02em;
        margin-bottom: 6px;
        line-height: 1.25;
    }
    
    .mck-subheader {
        font-size: 16px;
        color: #334155;
        margin-bottom: 24px;
        line-height: 1.5;
    }

    /* Executive Top Briefing Banner */
    .briefing-banner {
        background: #00205B;
        color: #FFFFFF;
        padding: 24px 30px;
        border-radius: 8px;
        border-left: 8px solid #C59B27; /* McKinsey Ochre Gold */
        margin-bottom: 26px;
        box-shadow: 0 4px 12px rgba(0, 32, 91, 0.1);
    }
    .briefing-banner h1 {
        color: #FFFFFF !important;
        font-size: 26px;
        font-weight: 800;
        margin: 0 0 6px 0;
    }
    .briefing-banner p {
        color: #E2E8F0 !important;
        font-size: 15px;
        margin: 0;
        line-height: 1.5;
    }

    /* High-Readability Form Field Labels */
    .stSelectbox label, .stSlider label {
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        margin-bottom: 6px !important;
    }

    /* Action Button - High Contrast, Large Text */
    div.stButton > button:first-child {
        background-color: #00205B !important;
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        letter-spacing: 0.03em !important;
        padding: 14px 32px !important;
        border: 2px solid #C59B27 !important;
        border-radius: 6px !important;
        box-shadow: 0 4px 10px rgba(0, 32, 91, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #0A192F !important;
        color: #FEF08A !important;
        border-color: #FBBF24 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 32, 91, 0.3) !important;
    }

    /* Clean Card Containers */
    .card-box {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        padding: 20px 24px;
        margin-bottom: 18px;
    }
    .card-header-label {
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #00205B;
        margin-bottom: 8px;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 4px;
    }

    /* Risk Factors Callouts (Large, Clear) */
    .factor-item {
        font-size: 14.5px;
        font-weight: 600;
        padding: 10px 14px;
        border-radius: 4px;
        margin-bottom: 8px;
        line-height: 1.45;
    }
    .factor-positive {
        background-color: #EFF6FF;
        color: #00205B;
        border-left: 5px solid #00205B;
    }
    .factor-negative {
        background-color: #FEFCE8;
        color: #854D0E;
        border-left: 5px solid #D97706;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. MODEL LOADING & INITIALIZATION
# ==============================================================================
@st.cache_resource(show_spinner="Initializing credit risk model...")
def load_scoring_model():
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)

model = load_scoring_model()

# ==============================================================================
# 3. HIGH-READABILITY DROPDOWN MAPPINGS (Clear English, Zero Math Codes)
# ==============================================================================
CHECKING_MAP = {
    "Overdrawn Account / Negative (< 0 DM)": "<0",
    "Modest Balance (0 to 200 DM)": "0<=X<200",
    "Substantial Liquidity (≥ 200 DM)": ">=200",
    "No Active Checking Account": "no checking"
}

SAVINGS_MAP = {
    "Minimal Emergency Fund (< 100 DM)": "<100",
    "Modest Savings Buffer (100 to 500 DM)": "100<=X<500",
    "Healthy Savings Reserves (500 to 1,000 DM)": "500<=X<1000",
    "Substantial Savings Reserves (≥ 1,000 DM)": ">=1000",
    "No Known Savings Account": "no known savings"
}

EMPLOYMENT_MAP = {
    "Entry-Level / Under 1 Year Tenure": "<1",
    "1 to 4 Years (Established)": "1<=X<4",
    "4 to 7 Years (Stable Career)": "4<=X<7",
    "7+ Years (Senior / Long-Term Tenured)": ">=7",
    "Currently Unemployed": "unemployed"
}

PURPOSE_MAP = {
    "Consumer Electronics & Home Appliances": "radio/tv",
    "New Automobile Purchase": "new car",
    "Pre-Owned Automobile Purchase": "used car",
    "Furniture & Home Improvement": "furniture/equipment",
    "Small Business Operations & Working Capital": "business",
    "Education & Professional Development": "education",
    "Home Repairs & Upgrades": "repairs",
    "Other Personal Credit Requirements": "other"
}

HOUSING_MAP = {
    "Owner-Occupied (Mortgaged or Freehold)": "own",
    "Tenant (Rented Residential Property)": "rent",
    "Family Provided / Employer Housing": "for free"
}

# ==============================================================================
# 4. SIDEBAR NAVIGATION & ACADEMIC CREDENTIALS
# ==============================================================================
with st.sidebar:
    st.markdown("""
        <div style="padding: 10px 0 16px 0;">
            <div style="font-size: 22px; font-weight: 800; color: #00205B; letter-spacing: -0.01em;">
                🏛️ Apex Underwrite
            </div>
            <div style="font-size: 13px; font-weight: 600; color: #64748B;">
                Commercial Credit Risk Platform
            </div>
        </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Select Page",
        [
            "1. Executive Overview & Strategy",
            "2. Portfolio Evidence & Insights",
            "3. Credit Underwriting Predictor"
        ]
    )

    st.markdown("---")
    st.markdown("""
        <div style="font-size: 13px; color: #334155; line-height: 1.6;">
            <strong>Academic Credentials:</strong><br>
            • <strong>Jain (Deemed-to-be University)</strong><br>
            • CMS Business School | Class: <strong>FBA-03</strong><br>
            • <strong>Akshit Singh</strong> (USN: 25MBAR0401)<br>
            • <strong>Vinay Tiwari</strong> (USN: 25MBAR0247)<br>
            • Course: MLBA – MBA Sem III
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# PAGE 1: EXECUTIVE OVERVIEW & STRATEGY
# ==============================================================================
if page == "1. Executive Overview & Strategy":
    st.markdown("""
        <div class="briefing-banner">
            <h1>Executive Strategy Briefing: Retail Credit Underwriting</h1>
            <p>A supervised machine learning decision framework designed to evaluate loan applicants, quantify default risk, and prevent Non-Performing Assets (NPAs).</p>
        </div>
    """, unsafe_allow_html=True)

    # 4 Large, High-Legibility KPI Cards
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric(label="HISTORICAL APPLICANTS", value="1,000", help="Historic loan applicants in German Credit dataset")
    with k2:
        st.metric(label="PORTFOLIO DEFAULT RATE", value="30.0%", help="300 historical default events")
    with k3:
        st.metric(label="DEFAULTER CATCH RATE", value="71.7%", delta="Recall Score", help="Catches 72% of all potential defaulters")
    with k4:
        st.metric(label="DECISION STRATEGY", value="3 Tiers", help="Approve, Review, Decline")

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns([1.5, 1.2])

    with c1:
        with st.container(border=True):
            st.markdown("### ⚖️ The Asymmetric Cost of Lending Errors")
            st.write("""
            In banking credit underwriting, classification errors have profoundly unequal consequences:
            """)
            st.error("""
            **Type II Error (False Negative — Capital Destruction):**  
            Approving a borrower who defaults. The bank loses **100% of the loan principal** plus recovery and legal fees ($5,000 to $10,000+ per default).
            """)
            st.warning("""
            **Type I Error (False Positive — Opportunity Cost):**  
            Rejecting a creditworthy borrower. The bank forfeits only the **net interest margin (6% to 10%)** and risks relationship friction.
            """)
            st.markdown("""
            **Strategic Takeaway:**  
            Missing a bad loan is **10 to 15 times more damaging** to bank reserves than turning down a good applicant. Hence, our Random Forest classifier is configured with **balanced penalty weights (`class_weight='balanced'`)**, achieving **71.7% Recall on Defaulters** to protect Tier-1 bank capital.
            """)

    with c2:
        with st.container(border=True):
            st.markdown("### 📋 Three Underwriting Policy Tiers")
            
            st.success("""
            **🟢 TIER 1: PRIME APPROVAL (Risk < 35%)**  
            Fast-track straight-through processing. Prime interest rate (+1.25% margin). No collateral or guarantor required.
            """)
            
            st.warning("""
            **🟡 TIER 2: CONDITIONAL REVIEW (35% – 55% Risk)**  
            Sensitivity zone. Counter-offer with a shorter loan tenure (< 18 months), require an employed co-signer, or apply a risk premium spread (+275 bps).
            """)
            
            st.error("""
            **🔴 TIER 3: PORTFOLIO DECLINE (Risk > 55%)**  
            Default probability exceeds bank risk tolerance. Issue adverse action notice or require 100% liquid cash-collateralized pledge.
            """)

# ==============================================================================
# PAGE 2: PORTFOLIO EVIDENCE & INSIGHTS (EDA)
# ==============================================================================
elif page == "2. Portfolio Evidence & Insights":
    st.markdown("""
        <div class="briefing-banner">
            <h1>Portfolio Evidence & Solvency Indicators</h1>
            <p>Empirical evidence extracted from historical German Credit data revealing the primary drivers of loan default.</p>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "Exhibit 1: Checking Account Balance",
        "Exhibit 2: Loan Tenure & Duration",
        "Exhibit 3: Overall Portfolio Breakdown"
    ])

    base_img_path = os.path.join(os.path.dirname(__file__), "images")

    with tab1:
        st.markdown("### Exhibit 1: Checking Account Liquidity — The Strongest Early Warning Signal")
        col_img, col_txt = st.columns([1.2, 1])
        with col_img:
            img_path = os.path.join(base_img_path, "fig2_checking_vs_default.png")
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.info("Chart available in repository.")
        with col_txt:
            with st.container(border=True):
                st.markdown("#### 💡 Executive Finding:")
                st.markdown("""
                * Applicants with **negative or overdrawn checking balances (`< 0 DM`)** suffer a default rate approaching **49.3%**.
                * Applicants maintaining reserves of **≥ 200 DM** experience default rates below **14.5%**.
                
                **Underwriting Policy Action:**  
                Liquid cash reserves act as the primary defense against immediate insolvency. Unsecured personal credit should be denied to overdrawn account holders unless secured by liquid deposits.
                """)

    with tab2:
        st.markdown("### Exhibit 2: Loan Tenure as a Multiplier of Default Exposure")
        col_img, col_txt = st.columns([1.2, 1])
        with col_img:
            img_path = os.path.join(base_img_path, "fig3_duration_vs_risk.png")
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.info("Chart available in repository.")
        with col_txt:
            with st.container(border=True):
                st.markdown("#### 💡 Executive Finding:")
                st.markdown("""
                * The median loan tenure for **defaulting borrowers is 30 months**, compared to **18 months** for repayers.
                * Longer tenures exponentially increase exposure to personal crises (unemployment, health shocks, divorce).
                
                **Underwriting Policy Action:**  
                For borderline credit applicants, loan officers should systematically offer a **tenure reduction (under 18–24 months)** to contain repayment risk.
                """)

    with tab3:
        st.markdown("### Exhibit 3: Historical Training Population Distribution")
        col_img, col_txt = st.columns([1.2, 1])
        with col_img:
            img_path = os.path.join(base_img_path, "fig1_risk_distribution.png")
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.info("Chart available in repository.")
        with col_txt:
            with st.container(border=True):
                st.markdown("#### 💡 Statistical Takeaway:")
                st.markdown("""
                * **700 Good Performing Loans (70.0%)** vs. **300 Bad Defaulting Loans (30.0%)**.
                * In raw machine learning, a lazy model could predict all applicants are "Good" and achieve 70% accuracy while missing 100% of defaulters!
                * By tuning Random Forest with **balanced penalty weights**, our model actively hunts down defaulters and intercepts 71.7% of high-risk applicants.
                """)

# ==============================================================================
# PAGE 3: CREDIT UNDERWRITING PREDICTOR
# ==============================================================================
elif page == "3. Credit Underwriting Predictor":
    st.markdown("""
        <div class="briefing-banner">
            <h1>Point-of-Sale Underwriting Decision Engine</h1>
            <p>Input applicant credit profile attributes to generate an instant actuarial score, risk category, and underwriting directive.</p>
        </div>
    """, unsafe_allow_html=True)

    with st.form("underwriting_input_form"):
        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.markdown("#### 🏦 1. Liquidity & Financial Standing")
                
                checking_label = st.selectbox(
                    "Checking Account Balance",
                    options=list(CHECKING_MAP.keys()),
                    index=1,
                    help="Operating liquid reserves in active checking account"
                )
                
                savings_label = st.selectbox(
                    "Savings & Deposit Buffer",
                    options=list(SAVINGS_MAP.keys()),
                    index=1,
                    help="Total savings buffer available across deposit accounts"
                )

                housing_label = st.selectbox(
                    "Residential Ownership Status",
                    options=list(HOUSING_MAP.keys()),
                    index=0,
                    help="Ownership status of primary residence"
                )

        with col2:
            with st.container(border=True):
                st.markdown("#### 📄 2. Loan Parameters & Demographics")
                
                credit_amount = st.slider(
                    "Requested Loan Principal Amount",
                    min_value=250,
                    max_value=15000,
                    value=3200,
                    step=250,
                    format="%d DM",
                    help="Total principal requested"
                )
                
                duration = st.slider(
                    "Repayment Tenure (Amortization Horizon)",
                    min_value=6,
                    max_value=60,
                    value=24,
                    step=2,
                    format="%d Months",
                    help="Repayment tenure in months"
                )

                age = st.slider(
                    "Borrower Age (Years)",
                    min_value=18,
                    max_value=75,
                    value=34,
                    format="%d Years",
                    help="Age of primary applicant"
                )

                employment_label = st.selectbox(
                    "Employment Tenure (Current Employer)",
                    options=list(EMPLOYMENT_MAP.keys()),
                    index=1,
                    help="Continuous employment length"
                )

                purpose_label = st.selectbox(
                    "Designated Loan Purpose",
                    options=list(PURPOSE_MAP.keys()),
                    index=0,
                    help="Intended use for borrowed capital"
                )

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("⚡ RUN CREDIT ASSESSMENT & GENERATE DIRECTIVE", use_container_width=True)

    # Output Evaluation
    if submitted:
        if model is None:
            st.error("Scoring model (model.pkl) is not loaded. Please verify deployment.")
        else:
            raw_checking = CHECKING_MAP[checking_label]
            raw_savings = SAVINGS_MAP[savings_label]
            raw_employment = EMPLOYMENT_MAP[employment_label]
            raw_purpose = PURPOSE_MAP[purpose_label]
            raw_housing = HOUSING_MAP[housing_label]

            input_df = pd.DataFrame([{
                'checking_status': raw_checking,
                'duration': duration,
                'credit_amount': credit_amount,
                'savings_status': raw_savings,
                'employment': raw_employment,
                'age': age,
                'housing': raw_housing,
                'purpose': raw_purpose
            }])

            prob_default = float(model.predict_proba(input_df)[0][1])
            prob_good = 1.0 - prob_default
            ref_id = f"APP-{datetime.datetime.now().strftime('%Y%m%d')}-{abs(hash(str(credit_amount) + str(age))) % 10000:04d}"

            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            st.markdown("## 📋 Underwriting Evaluation Dossier")

            # Clean Metadata Bar
            st.info(f"**Application Reference:** `{ref_id}` | **Evaluated Facility:** `{credit_amount:,} DM` over `{duration} Months` | **Timestamp:** `{datetime.datetime.now().strftime('%d-%b-%Y %H:%M UTC')}`")

            out_col1, out_col2 = st.columns([1.2, 1])

            with out_col1:
                if prob_default < 0.35:
                    st.success(f"""
                    ### ✅ TIER 1: PRIME APPROVAL (Straight-Through)
                    **Actuarial Default Probability:** **{prob_default:.1%}** (Low Risk)
                    """)
                    with st.container(border=True):
                        st.markdown("#### 📌 Underwriting Directives:")
                        st.markdown("""
                        * **Disbursement Status:** Approved for instant automated disbursement.
                        * **Pricing Margin:** Prime base rate + 1.25% margin.
                        * **Collateral Requirement:** Unsecured facility; no secondary pledge or co-signer required.
                        * **Repayment Mandate:** Standard monthly direct debit covenant.
                        """)

                elif prob_default <= 0.55:
                    st.warning(f"""
                    ### ⚠️ TIER 2: CONDITIONAL REVIEW / COUNTER-OFFER
                    **Actuarial Default Probability:** **{prob_default:.1%}** (Moderate Sensitivity Band)
                    """)
                    with st.container(border=True):
                        st.markdown("#### 📌 Prescriptive Counter-Offer Options:")
                        st.markdown(f"""
                        * **Disbursement Status:** Suspended pending senior credit underwriter review.
                        * **Recommended Restructuring:**
                          1. Compress tenure from **{duration} months** to **{max(12, int(duration * 0.7))} months**.
                          2. Require an employed co-signer or verifiable liquid guarantor.
                          3. Apply risk-adjusted spread (+275 bps over prime).
                        """)

                else:
                    st.error(f"""
                    ### ❌ TIER 3: APPLICATION DECLINED
                    **Actuarial Default Probability:** **{prob_default:.1%}** (High Delinquency Exposure)
                    """)
                    with st.container(border=True):
                        st.markdown("#### 📌 Adverse Action Directives:")
                        st.markdown("""
                        * **Disbursement Status:** Declined under standard unsecured retail criteria.
                        * **Risk Rationale:** Delinquency likelihood exceeds institutional risk appetite.
                        * **Alternative Pathway:** Offer 100% liquid cash-collateralized structure (fixed deposit lien) to proceed.
                        """)

            with out_col2:
                with st.container(border=True):
                    st.markdown("#### 🎯 Solvency vs. Delinquency Probability")
                    
                    # Large, Ultra-Readable Chart
                    fig, ax = plt.subplots(figsize=(7.0, 3.2), dpi=140)
                    fig.patch.set_facecolor('#FFFFFF')
                    ax.set_facecolor('#FFFFFF')
                    
                    categories = ['Repayment\nConfidence', 'Default\nExposure']
                    scores = [prob_good * 100, prob_default * 100]
                    colors = ['#00205B', '#C59B27'] # Deep Navy & Warm Ochre Gold
                    
                    bars = ax.barh(categories, scores, color=colors, height=0.48, edgecolor='none')
                    ax.set_xlim(0, 120)
                    ax.set_xlabel('Actuarial Probability (%)', fontsize=12, color='#00205B', fontweight='bold')
                    ax.tick_params(colors='#0F172A', labelsize=12)
                    
                    for bar in bars:
                        w = bar.get_width()
                        ax.text(w + 3, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', 
                                va='center', ha='left', fontweight='bold', color='#00205B', fontsize=13)
                    
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.spines['left'].set_color('#CBD5E1')
                    ax.spines['bottom'].set_color('#CBD5E1')
                    ax.grid(axis='x', linestyle='--', alpha=0.4, color='#94A3B8')
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close(fig)

                # Key Drivers Box
                with st.container(border=True):
                    st.markdown("#### 🔍 Detected Profile Drivers:")

                    if raw_checking == "<0":
                        st.markdown('<div class="factor-item factor-negative">⚠️ Overdrawn / Negative checking balance indicates immediate cash flow stress.</div>', unsafe_allow_html=True)
                    elif raw_checking in [">=200", "no checking"]:
                        st.markdown('<div class="factor-item factor-positive">✅ Solid current account liquidity provides strong repayment buffer.</div>', unsafe_allow_html=True)

                    if duration > 36:
                        st.markdown('<div class="factor-item factor-negative">⚠️ Extended tenure (>36 months) multiplies exposure to economic cycle volatility.</div>', unsafe_allow_html=True)
                    elif duration <= 18:
                        st.markdown('<div class="factor-item factor-positive">✅ Compact loan horizon (≤18 months) minimizes default exposure.</div>', unsafe_allow_html=True)

                    if raw_savings in [">=1000", "500<=X<1000"]:
                        st.markdown('<div class="factor-item factor-positive">✅ Substantial savings buffer acts as reliable safety net against unexpected personal shocks.</div>', unsafe_allow_html=True)
                    elif raw_savings == "<100":
                        st.markdown('<div class="factor-item factor-negative">⚠️ Minimal emergency savings reserve leaves applicant vulnerable to disruption.</div>', unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import datetime

# ==============================================================================
# 1. PAGE CONFIGURATION & DESIGN SYSTEM
# ==============================================================================
st.set_page_config(
    page_title="Apex Underwrite | Commercial Credit Risk Engine",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Institutional CSS Design System with Micro-animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global Typography & Palette */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #0F172A;
    }

    /* Smooth page fade-in animation */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .animate-in {
        animation: fadeInUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Executive Top App Banner - Blue & Gold/Yellow */
    .brand-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 60%, #172554 100%);
        border-radius: 14px;
        padding: 24px 30px;
        color: #FFFFFF;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.25);
        border: 1px solid rgba(245, 158, 11, 0.35);
        border-left: 6px solid #F59E0B;
    }
    .brand-banner h1 {
        font-size: 26px;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
        color: #FFFFFF;
    }
    .brand-banner p {
        font-size: 14px;
        color: #CBD5E1;
        margin: 6px 0 0 0;
        font-weight: 400;
    }
    .gold-badge {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid #F59E0B;
        color: #FDE047;
        border-radius: 8px;
        padding: 6px 14px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.03em;
    }

    /* Live Operational Status Pill - Blue & Yellow */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(30, 58, 138, 0.08);
        color: #1E3A8A;
        font-size: 12px;
        font-weight: 700;
        padding: 5px 14px;
        border-radius: 20px;
        border: 1.5px solid #F59E0B;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #F59E0B;
        border-radius: 50%;
        box-shadow: 0 0 8px #F59E0B;
    }

    /* Institutional Cards - Blue & Yellow accents */
    .fintech-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-top: 3px solid #1E3A8A;
        border-radius: 12px;
        padding: 20px 22px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px -2px rgba(15, 23, 42, 0.05);
        transition: all 0.25s ease;
    }
    .fintech-card:hover {
        border-color: #F59E0B;
        border-top: 3px solid #F59E0B;
        box-shadow: 0 10px 25px -4px rgba(30, 58, 138, 0.12);
        transform: translateY(-2px);
    }
    .card-label {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #1E3A8A;
        margin-bottom: 6px;
    }
    .card-value {
        font-size: 22px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
    }

    /* Decision Badges */
    .badge-approved {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border: 1.5px solid #1E3A8A;
        color: #1E3A8A;
        padding: 16px 20px;
        border-radius: 10px;
        font-weight: 700;
        margin-bottom: 14px;
        box-shadow: 0 4px 12px -2px rgba(30, 58, 138, 0.15);
    }
    .badge-conditional {
        background: linear-gradient(135deg, #FEFCE8 0%, #FEF08A 100%);
        border: 1.5px solid #EAB308;
        color: #854D0E;
        padding: 16px 20px;
        border-radius: 10px;
        font-weight: 700;
        margin-bottom: 14px;
        box-shadow: 0 4px 12px -2px rgba(234, 179, 8, 0.2);
    }
    .badge-declined {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border: 1.5px solid #EF4444;
        color: #991B1B;
        padding: 16px 20px;
        border-radius: 10px;
        font-weight: 700;
        margin-bottom: 14px;
    }

    /* Factor tags */
    .tag-positive {
        background: #EFF6FF;
        color: #1E3A8A;
        border: 1px solid #BFDBFE;
        border-left: 4px solid #1E3A8A;
        padding: 7px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        margin: 5px 0;
        display: block;
    }
    .tag-negative {
        background: #FEFCE8;
        color: #854D0E;
        border: 1px solid #FEF08A;
        border-left: 4px solid #EAB308;
        padding: 7px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        margin: 5px 0;
        display: block;
    }

    /* Primary Action Button - Royal Blue with Warm Gold Accents */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        color: #FFFFFF;
        font-weight: 700;
        font-size: 15px;
        border: 1.5px solid #F59E0B;
        border-radius: 8px;
        padding: 12px 28px;
        box-shadow: 0 4px 14px 0 rgba(30, 58, 138, 0.35);
        transition: all 0.25s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #172554 0%, #1E3A8A 100%);
        border-color: #FDE047;
        color: #FEF08A;
        box-shadow: 0 6px 20px 0 rgba(245, 158, 11, 0.45);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. MODEL CACHING & INITIALIZATION
# ==============================================================================
@st.cache_resource(show_spinner="Loading scoring pipeline...")
def load_scoring_model():
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)

model = load_scoring_model()

# ==============================================================================
# 3. PROFESSIONAL BANKING VOCABULARY MAPPINGS
# ==============================================================================
CHECKING_MAP = {
    "Overdrawn / Deficit (< 0 DM)": "<0",
    "Modest Balance (0 to 200 DM)": "0<=X<200",
    "Substantial Liquidity (≥ 200 DM)": ">=200",
    "No Active Checking Account with Bank": "no checking"
}

SAVINGS_MAP = {
    "Low Emergency Fund (< 100 DM)": "<100",
    "Modest Savings Buffer (100 to 500 DM)": "100<=X<500",
    "Healthy Savings (500 to 1,000 DM)": "500<=X<1000",
    "Substantial Reserves (≥ 1,000 DM)": ">=1000",
    "No Known Savings Account": "no known savings"
}

EMPLOYMENT_MAP = {
    "Entry-Level / Under 1 Year": "<1",
    "1 to 4 Years (Established)": "1<=X<4",
    "4 to 7 Years (Stable Career)": "4<=X<7",
    "7+ Years (Senior / Long-Term Tenured)": ">=7",
    "Currently Unemployed": "unemployed"
}

PURPOSE_MAP = {
    "Consumer Electronics & Appliances": "radio/tv",
    "New Automobile Purchase": "new car",
    "Pre-Owned Automobile": "used car",
    "Furniture & Home Improvement": "furniture/equipment",
    "Small Business Working Capital": "business",
    "Higher Education & Professional Training": "education",
    "Home Repairs & Upgrades": "repairs",
    "Other Personal Financing": "other"
}

HOUSING_MAP = {
    "Homeowner (Self-Owned / Mortgaged)": "own",
    "Tenant (Rented Property)": "rent",
    "Free / Employer / Family Housing": "for free"
}

# ==============================================================================
# 4. SIDEBAR NAVIGATION & PORTAL BRANDING
# ==============================================================================
with st.sidebar:
    st.markdown("""
        <div style="padding: 10px 0 20px 0;">
            <div style="font-size: 20px; font-weight: 800; color: #0F172A; letter-spacing: -0.02em;">
                🏛️ Apex Underwrite
            </div>
            <div style="font-size: 12px; color: #64748B; margin-top: 2px;">
                Commercial Credit Risk Platform
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="status-pill">
            <span class="status-dot"></span>
            Production Model v1.2 Active
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "Executive Overview",
            "Portfolio Analytics (EDA)",
            "Underwriting Decision Engine"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
        <div style="font-size: 11px; color: #64748B; line-height: 1.6;">
            <strong>Institutional Governance:</strong><br>
            • Framework: Scikit-Learn Pipeline<br>
            • Estimator: Balanced Random Forest<br>
            • Primary Metric: Recall on Defaulters (71.7%)<br>
            • Dataset: Statlog German Credit Data<br>
            • Academic Course: MLBA – MBA
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# PAGE 1: EXECUTIVE OVERVIEW
# ==============================================================================
if page == "Executive Overview":
    st.markdown("""
        <div class="brand-banner animate-in">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h1>AI-Driven Credit Default Risk Analyzer</h1>
                    <p>Automated loan origination and risk-stratification decision system for commercial retail banking.</p>
                </div>
                <div class="gold-badge">
                    Decision Tier: Tier-1 Credit
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Top KPI summary cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown("""
            <div class="fintech-card">
                <div class="card-label">Training Population</div>
                <div class="card-value">1,000</div>
                <div style="font-size: 12px; color: #64748B; margin-top: 4px;">Historical Loan Records</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi2:
        st.markdown("""
            <div class="fintech-card">
                <div class="card-label">Target Repayer Ratio</div>
                <div class="card-value">70.0%</div>
                <div style="font-size: 12px; color: #10B981; margin-top: 4px;">700 Performing Loans</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown("""
            <div class="fintech-card">
                <div class="card-label">Defaulter Recall</div>
                <div class="card-value">71.7%</div>
                <div style="font-size: 12px; color: #3B82F6; margin-top: 4px;">High-Risk Catch Rate</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi4:
        st.markdown("""
            <div class="fintech-card">
                <div class="card-label">Decision Strategy</div>
                <div class="card-value">Tri-Tier</div>
                <div style="font-size: 12px; color: #64748B; margin-top: 4px;">Approve • Review • Decline</div>
            </div>
        """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1.6, 1])

    with col_left:
        st.markdown("### 🏛️ 1. Business Challenge & Institutional Context")
        st.write("""
        Commercial lenders generate core operating margin from interest spreads. However, borrower delinquency 
        and write-offs directly deplete Tier-1 regulatory capital and generate Non-Performing Assets (NPAs).
        
        Traditional credit underwriting relied on rigid heuristic rulebooks or slow manual committee approvals, 
        introducing processing latency and subjective bias. This platform automates the initial screening tier, 
        empowering loan officers with data-driven probabilistic scoring.
        """)

        st.markdown("### ⚖️ 2. The Asymmetric Cost of Lending Errors")
        st.write("""
        Standard machine learning optimization assumes symmetric costs between false positives and false negatives. 
        In credit underwriting, this assumption is fundamentally flawed:
        """)

        st.markdown("""
        * **False Negative (Critical Capital Loss):** Approving a borrower who subsequently defaults. The bank suffers 
          a direct balance sheet loss equal to 100% of unrecovered principal plus workout costs.
        * **False Positive (Opportunity Cost):** Declining or delaying a creditworthy borrower. The bank forfeits the 
          interest margin (typically 6%–10%) and risks customer churn.
        
        **Strategic Caliber:** Our Random Forest model is trained with **balanced penalty weights (`class_weight='balanced'`)**, 
        prioritizing **Recall on Defaulters (71.7%)** to rigorously protect institutional capital.
        """)

    with col_right:
        st.markdown("### 📋 Underwriting Policy Rules")
        st.markdown("""
            <div class="fintech-card">
                <div style="font-weight: 700; color: #065F46; font-size: 14px; margin-bottom: 4px;">
                    🟢 Green Tier: Default Probability &lt; 35%
                </div>
                <div style="font-size: 13px; color: #475569;">
                    <strong>Recommendation: Instant Approval.</strong> Fast-track straight-through processing at standard prime margins. No additional guarantor or security pledge required.
                </div>
            </div>
            
            <div class="fintech-card">
                <div style="font-weight: 700; color: #92400E; font-size: 14px; margin-bottom: 4px;">
                    🟡 Amber Tier: Default Probability 35% – 55%
                </div>
                <div style="font-size: 13px; color: #475569;">
                    <strong>Recommendation: Enhanced Scrutiny / Counter-Offer.</strong> Moderate credit sensitivity. Underwriters counteroffer with shorter tenure (&lt; 18 months), mandate co-signers, or request collateral backing.
                </div>
            </div>

            <div class="fintech-card">
                <div style="font-weight: 700; color: #991B1B; font-size: 14px; margin-bottom: 4px;">
                    🔴 Red Tier: Default Probability &gt; 55%
                </div>
                <div style="font-size: 13px; color: #475569;">
                    <strong>Recommendation: Decline / Strict Escalation.</strong> Estimated loss expectation exceeds portfolio risk appetite. Decline application or require 100% liquid deposit pledge.
                </div>
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# PAGE 2: PORTFOLIO ANALYTICS (EDA)
# ==============================================================================
elif page == "Portfolio Analytics (EDA)":
    st.markdown("""
        <div class="brand-banner animate-in">
            <h1>Portfolio Analytics & Solvency Drivers</h1>
            <p>Empirical evidence extracted from historical German Credit portfolios informing model weights.</p>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "📊 Liquid Checking Solvency",
        "⏳ Repayment Horizon Risk",
        "🎯 Historical Class Distribution"
    ])

    base_img_path = os.path.join(os.path.dirname(__file__), "images")

    with tab1:
        st.markdown("#### Primary Predictor: Checking Account Liquidity Status")
        col_img, col_desc = st.columns([1.3, 1])
        with col_img:
            img_path = os.path.join(base_img_path, "fig2_checking_vs_default.png")
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.warning("Figure not found in repository.")
        with col_desc:
            st.markdown("""
            <div class="fintech-card">
                <div class="card-label">Executive Takeaway</div>
                <div style="font-size: 14px; line-height: 1.6; color: #334155;">
                    • Applicants with <strong>overdrawn or negative checking balances (&lt; 0 DM)</strong> exhibit default rates approaching <strong>49.3%</strong>.<br><br>
                    • In contrast, applicants with healthy liquid buffers (<strong>&ge; 200 DM</strong>) maintain default rates below <strong>14.5%</strong>.<br><br>
                    • <strong>Policy Guidance:</strong> Current account liquidity serves as the bank's strongest immediate barometer against imminent cash insolvency.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("#### Duration Exposure: How Time Horizons Multiply Risk")
        col_img, col_desc = st.columns([1.3, 1])
        with col_img:
            img_path = os.path.join(base_img_path, "fig3_duration_vs_risk.png")
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.warning("Figure not found in repository.")
        with col_desc:
            st.markdown("""
            <div class="fintech-card">
                <div class="card-label">Tenure Risk Analysis</div>
                <div style="font-size: 14px; line-height: 1.6; color: #334155;">
                    • The median loan duration for defaulting accounts is <strong>30 months</strong>, compared to <strong>18 months</strong> for fully performing loans.<br><br>
                    • Extended amortization schedules expose the credit agreement to macroeconomic cycles, interest shocks, and personal life vulnerabilities.<br><br>
                    • <strong>Underwriter Guideline:</strong> Restricting unsecured exposure to under 24 months reduces default susceptibility by over 30%.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("#### Macro Portfolio Profile & Training Population")
        col_img, col_desc = st.columns([1.3, 1])
        with col_img:
            img_path = os.path.join(base_img_path, "fig1_risk_distribution.png")
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.warning("Figure not found in repository.")
        with col_desc:
            st.markdown("""
            <div class="fintech-card">
                <div class="card-label">Sample Distribution</div>
                <div style="font-size: 14px; line-height: 1.6; color: #334155;">
                    • <strong>Performing Loans (Good):</strong> 700 records (70.0%)<br>
                    • <strong>Defaulted Accounts (Bad):</strong> 300 records (30.0%)<br><br>
                    • <strong>Statistical Calibration:</strong> Standard unweighted classifiers naturally favor the 70% majority class. Introducing stratified holdout testing and balanced loss matrices prevents complacency on the 30% defaulter subset.
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# PAGE 3: UNDERWRITING DECISION ENGINE
# ==============================================================================
elif page == "Underwriting Decision Engine":
    st.markdown("""
        <div class="brand-banner animate-in">
            <h1>Point-of-Sale Underwriting Engine</h1>
            <p>Enter applicant credit profile attributes to generate an instant actuarial score and policy recommendation.</p>
        </div>
    """, unsafe_allow_html=True)

    # Input Form with Clean Grouping
    with st.form("applicant_evaluation_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("##### 🏦 1. Borrower Liquid Reserves")
            
            checking_label = st.selectbox(
                "Checking Account Balance",
                options=list(CHECKING_MAP.keys()),
                index=1,
                help="Current liquid reserves held in primary operating or checking account."
            )
            
            savings_label = st.selectbox(
                "Savings & Deposit Buffer",
                options=list(SAVINGS_MAP.keys()),
                index=1,
                help="Total liquid savings available across rainy-day deposits and time accounts."
            )

            housing_label = st.selectbox(
                "Residential Status",
                options=list(HOUSING_MAP.keys()),
                index=0,
                help="Ownership stability of current residence."
            )

        with col2:
            st.markdown("##### 📄 2. Loan Request Terms")
            
            credit_amount = st.slider(
                "Requested Loan Principal Amount",
                min_value=250,
                max_value=15000,
                value=3200,
                step=250,
                format="%d DM",
                help="Total borrowing principal requested by the client."
            )
            
            duration = st.slider(
                "Repayment Tenure (Loan Term)",
                min_value=6,
                max_value=60,
                value=24,
                step=2,
                format="%d Months",
                help="Scheduled amortization period in months."
            )

            purpose_label = st.selectbox(
                "Designated Loan Purpose",
                options=list(PURPOSE_MAP.keys()),
                index=0,
                help="Commercial or personal intent for borrowed capital."
            )

        with col3:
            st.markdown("##### 👤 3. Applicant Career & Stability")
            
            age = st.slider(
                "Borrower Age",
                min_value=18,
                max_value=75,
                value=34,
                format="%d Years",
                help="Age of primary applicant."
            )

            employment_label = st.selectbox(
                "Tenure at Current Employer",
                options=list(EMPLOYMENT_MAP.keys()),
                index=1,
                help="Length of unbroken service with primary employer or business."
            )

            st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("⚡ Run Credit Evaluation & Generate Dossier", use_container_width=True)

    # Output Evaluation
    if submitted:
        if model is None:
            st.error("Scoring pipeline (model.pkl) was not located on system path. Please train or deploy model.pkl.")
        else:
            # Map human labels back to model feature tokens
            raw_checking = CHECKING_MAP[checking_label]
            raw_savings = SAVINGS_MAP[savings_label]
            raw_employment = EMPLOYMENT_MAP[employment_label]
            raw_purpose = PURPOSE_MAP[purpose_label]
            raw_housing = HOUSING_MAP[housing_label]

            # Construct inference dataframe
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

            # Calculate continuous default probability
            prob_default = float(model.predict_proba(input_df)[0][1])
            prob_good = 1.0 - prob_default
            ref_id = f"APP-{datetime.datetime.now().strftime('%Y%m%d')}-{abs(hash(str(credit_amount) + str(age))) % 10000:04d}"

            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            st.markdown("### 📋 Executive Underwriting Dossier")

            # Top Meta Header
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; background: #F1F5F9; padding: 12px 18px; border-radius: 8px; border: 1px solid #CBD5E1; margin-bottom: 20px;">
                    <div><strong>Application Reference:</strong> <code>{ref_id}</code></div>
                    <div><strong>Evaluation Timestamp:</strong> {datetime.datetime.now().strftime('%d-%b-%Y %H:%M:%S UTC')}</div>
                    <div><strong>Requested Principal:</strong> {credit_amount:,} DM ({duration} Mo)</div>
                </div>
            """, unsafe_allow_html=True)

            out_left, out_right = st.columns([1.1, 1])

            with out_left:
                # Recommendation Card Logic
                if prob_default < 0.35:
                    st.markdown(f"""
                        <div class="badge-approved">
                            <div style="font-size: 18px; letter-spacing: -0.01em;">✅ TIER 1: APPROVED (STRAIGHT-THROUGH)</div>
                            <div style="font-size: 13px; font-weight: 500; margin-top: 6px; color: #064E3B;">
                                Default Probability: <strong>{prob_default:.1%}</strong> | Prime Lending Grade
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown("""
                        <div class="fintech-card">
                            <div class="card-label">Actionable Underwriting Directive</div>
                            <div style="font-size: 14px; line-height: 1.6;">
                                • <strong>Disbursement Status:</strong> Eligible for instant automated funding.<br>
                                • <strong>Pricing Margin:</strong> Prime base rate + 1.25% credit spread.<br>
                                • <strong>Collateralization:</strong> Unsecured facility; no secondary pledge or guarantor required.<br>
                                • <strong>Covenants:</strong> Standard monthly direct debit payment mandate.
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                elif prob_default <= 0.55:
                    st.markdown(f"""
                        <div class="badge-conditional">
                            <div style="font-size: 18px; letter-spacing: -0.01em;">⚠️ TIER 2: CONDITIONAL APPROVAL / MANUAL REVIEW</div>
                            <div style="font-size: 13px; font-weight: 500; margin-top: 6px; color: #78350F;">
                                Default Probability: <strong>{prob_default:.1%}</strong> | Heightened Exposure Zone
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown("""
                        <div class="fintech-card">
                            <div class="card-label">Prescriptive Underwriting Directive</div>
                            <div style="font-size: 14px; line-height: 1.6;">
                                • <strong>Disbursement Status:</strong> On hold pending secondary underwriter approval.<br>
                                • <strong>Recommended Counter-Offer:</strong>
                                  <br>&nbsp;&nbsp;1. Restructure tenure from <strong>""" + str(duration) + """ months</strong> to <strong>""" + str(max(12, int(duration * 0.7))) + """ months</strong>.
                                  <br>&nbsp;&nbsp;2. Require an employed co-signer or verifiable liquid guarantor.
                                  <br>&nbsp;&nbsp;3. Price with risk premium (+275 bps margin).
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                else:
                    st.markdown(f"""
                        <div class="badge-declined">
                            <div style="font-size: 18px; letter-spacing: -0.01em;">❌ TIER 3: DECLINED (EXCEEDS RISK APPETITE)</div>
                            <div style="font-size: 13px; font-weight: 500; margin-top: 6px; color: #7F1D1D;">
                                Default Probability: <strong>{prob_default:.1%}</strong> | Subprime Risk Profile
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown("""
                        <div class="fintech-card">
                            <div class="card-label">Adverse Action & Restructuring Directives</div>
                            <div style="font-size: 14px; line-height: 1.6;">
                                • <strong>Disbursement Status:</strong> Declined under standard unsecured retail criteria.<br>
                                • <strong>Risk Rationale:</strong> Actuarial probability of 90-day delinquency exceeds bank risk tolerance.<br>
                                • <strong>Alternative Pathway:</strong> Offer 100% asset-backed pledge (fixed deposit lien or vehicle encumbrance) to proceed.
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            with out_right:
                st.markdown("#### 🎯 Solvency vs. Delinquency Probability")
                
                # Modern styled horizontal chart
                fig, ax = plt.subplots(figsize=(5.5, 2.6), dpi=100)
                fig.patch.set_facecolor('#FFFFFF')
                ax.set_facecolor('#FFFFFF')
                
                categories = ['Repayment\nConfidence', 'Default\nExposure']
                scores = [prob_good * 100, prob_default * 100]
                colors = ['#1E3A8A', '#F59E0B']  # Royal Blue and Warm Yellow/Gold theme
                
                bars = ax.barh(categories, scores, color=colors, height=0.45, edgecolor='none')
                ax.set_xlim(0, 115)
                ax.set_xlabel('Probability Share (%)', fontsize=10, color='#64748B', fontweight='600')
                ax.tick_params(colors='#334155', labelsize=10)
                
                for bar in bars:
                    w = bar.get_width()
                    ax.text(w + 2.5, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', 
                            va='center', ha='left', fontweight='bold', color='#0F172A', fontsize=11)
                
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_color('#E2E8F0')
                ax.spines['bottom'].set_color('#E2E8F0')
                ax.grid(axis='x', linestyle='--', alpha=0.3, color='#94A3B8')
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

                # Key Drivers Detected Callouts
                st.markdown("<div style='font-size: 12px; font-weight: 700; color: #475569; margin: 12px 0 4px 0;'>DETECTED PROFILE INFLUENCERS:</div>", unsafe_allow_html=True)
                
                # Dynamic factors detected
                if raw_checking == "<0":
                    st.markdown('<div class="tag-negative">⚠️ Overdrawn / Negative checking balance signals immediate cash flow vulnerability.</div>', unsafe_allow_html=True)
                elif raw_checking in [">=200", "no checking"]:
                    st.markdown('<div class="tag-positive">✅ Solid current account liquidity provides strong repayment buffer.</div>', unsafe_allow_html=True)

                if duration > 36:
                    st.markdown('<div class="tag-negative">⚠️ Extended tenure (>36 months) multiplies exposure to economic cycle fluctuations.</div>', unsafe_allow_html=True)
                elif duration <= 18:
                    st.markdown('<div class="tag-positive">✅ Compact loan horizon (≤18 months) minimizes default exposure.</div>', unsafe_allow_html=True)

                if raw_savings in [">=1000", "500<=X<1000"]:
                    st.markdown('<div class="tag-positive">✅ Substantial savings buffer acts as reliable safety net against unexpected shocks.</div>', unsafe_allow_html=True)
                elif raw_savings == "<100":
                    st.markdown('<div class="tag-negative">⚠️ Minimal emergency savings reserve leaves applicant sensitive to financial disruption.</div>', unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import datetime

# ==============================================================================
# 1. MCKINSEY-INSPIRED DESIGN SYSTEM & EXECUTIVE TYPOGRAPHY
# ==============================================================================
st.set_page_config(
    page_title="Apex Underwrite | McKinsey-Style Credit Risk Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Legibility Consulting Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Merriweather:ital,wght@0,400;0,700;1,400&display=swap');

    /* Global Base Styling */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #0F172A;
        background-color: #FAFAFA;
    }

    /* Executive Editorial Headers */
    h1, h2, h3, .editorial-title {
        font-family: 'Merriweather', Georgia, serif !important;
        font-weight: 700;
        color: #00205B !important; /* McKinsey Signature Deep Navy */
        letter-spacing: -0.01em;
    }

    /* Subtle Entry Fade */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .mckinsey-view {
        animation: fadeIn 0.35s ease-out forwards;
    }

    /* Top Executive Briefing Banner */
    .mckinsey-banner {
        background: #00205B;
        border-bottom: 4px solid #C59B27; /* McKinsey Ochre Gold */
        border-radius: 6px;
        padding: 24px 28px;
        color: #FFFFFF;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0, 32, 91, 0.08);
    }
    .mckinsey-banner h1 {
        color: #FFFFFF !important;
        font-size: 26px;
        margin: 0;
        line-height: 1.25;
    }
    .mckinsey-banner p {
        color: #E2E8F0;
        font-size: 14px;
        margin: 8px 0 0 0;
        font-family: 'Inter', sans-serif;
    }

    /* Exhibit Box - Clean Editorial Paper Cards */
    .exhibit-card {
        background: #FFFFFF;
        border: 1px solid #D1D5DB;
        border-radius: 4px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .exhibit-header {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #00205B;
        border-bottom: 1px solid #E5E7EB;
        padding-bottom: 6px;
        margin-bottom: 12px;
        font-family: 'Inter', sans-serif;
    }
    .exhibit-kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #00205B;
        font-family: 'Inter', sans-serif;
        line-height: 1.1;
    }
    .exhibit-kpi-desc {
        font-size: 13px;
        color: #334155;
        margin-top: 6px;
        line-height: 1.4;
    }

    /* Status Indicators */
    .badge-gold {
        background: #FEF3C7;
        color: #92400E;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 3px;
        border: 1px solid #F59E0B;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    /* Decision Tiers (Clear, High Contrast) */
    .verdict-approved {
        background: #F0FDF4;
        border-left: 6px solid #16A34A;
        border-top: 1px solid #BBF7D0;
        border-right: 1px solid #BBF7D0;
        border-bottom: 1px solid #BBF7D0;
        padding: 16px 20px;
        border-radius: 4px;
        margin-bottom: 16px;
    }
    .verdict-conditional {
        background: #FFFBEB;
        border-left: 6px solid #D97706;
        border-top: 1px solid #FDE68A;
        border-right: 1px solid #FDE68A;
        border-bottom: 1px solid #FDE68A;
        padding: 16px 20px;
        border-radius: 4px;
        margin-bottom: 16px;
    }
    .verdict-declined {
        background: #FEF2F2;
        border-left: 6px solid #DC2626;
        border-top: 1px solid #FECACA;
        border-right: 1px solid #FECACA;
        border-bottom: 1px solid #FECACA;
        padding: 16px 20px;
        border-radius: 4px;
        margin-bottom: 16px;
    }

    /* Factor Callout Strips */
    .factor-positive {
        background: #F8FAFC;
        border-left: 4px solid #00205B;
        padding: 8px 14px;
        font-size: 13px;
        color: #0F172A;
        font-weight: 600;
        margin-bottom: 6px;
        border-radius: 2px;
    }
    .factor-negative {
        background: #FEFCE8;
        border-left: 4px solid #D97706;
        padding: 8px 14px;
        font-size: 13px;
        color: #78350F;
        font-weight: 600;
        margin-bottom: 6px;
        border-radius: 2px;
    }

    /* McKinsey Style Action Button */
    div.stButton > button:first-child {
        background-color: #00205B !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
        border: 2px solid #C59B27 !important;
        border-radius: 3px !important;
        padding: 12px 28px !important;
        box-shadow: 0 2px 4px rgba(0, 32, 91, 0.15) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #0A192F !important;
        color: #FEF08A !important;
        border-color: #FBBF24 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(0, 32, 91, 0.25) !important;
    }

    /* Form Section Dividers */
    .form-section-title {
        font-family: 'Merriweather', Georgia, serif;
        font-size: 15px;
        font-weight: 700;
        color: #00205B;
        border-bottom: 1.5px solid #00205B;
        padding-bottom: 4px;
        margin-bottom: 14px;
    }

    /* High-contrast widget labels */
    .stSelectbox label, .stSlider label {
        font-weight: 600 !important;
        color: #0F172A !important;
        font-size: 13px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. MODEL LOADING & CACHING
# ==============================================================================
@st.cache_resource(show_spinner="Initializing scoring engine...")
def load_scoring_model():
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)

model = load_scoring_model()

# ==============================================================================
# 3. EXECUTIVE-GRADE VOCABULARY MAPPINGS (Zero Code-Jargon)
# ==============================================================================
CHECKING_MAP = {
    "Overdrawn Account (< 0 DM)": "<0",
    "Modest Operating Liquidity (0 to 200 DM)": "0<=X<200",
    "Substantial Cash Reserves (≥ 200 DM)": ">=200",
    "No Active Checking Account with Bank": "no checking"
}

SAVINGS_MAP = {
    "Minimal Emergency Fund (< 100 DM)": "<100",
    "Modest Savings Balance (100 to 500 DM)": "100<=X<500",
    "Healthy Savings Buffer (500 to 1,000 DM)": "500<=X<1000",
    "Substantial Capital Reserves (≥ 1,000 DM)": ">=1000",
    "No Verifiable Savings Records": "no known savings"
}

EMPLOYMENT_MAP = {
    "Entry-Level / Under 1 Year Tenure": "<1",
    "1 to 4 Years (Established)": "1<=X<4",
    "4 to 7 Years (Mid-Career Stability)": "4<=X<7",
    "7+ Years (Senior / Long-Term Tenured)": ">=7",
    "Currently Unemployed": "unemployed"
}

PURPOSE_MAP = {
    "Consumer Electronics & Household Goods": "radio/tv",
    "New Automobile Acquisition": "new car",
    "Pre-Owned Automobile Acquisition": "used car",
    "Home Furnishings & Improvements": "furniture/equipment",
    "Small Business Operations & Working Capital": "business",
    "Education & Professional Development": "education",
    "Property Repairs & Maintenance": "repairs",
    "Other Personal Credit Requirements": "other"
}

HOUSING_MAP = {
    "Owner-Occupied (Mortgaged or Freehold)": "own",
    "Tenant (Rented Residential Property)": "rent",
    "Family Provided / Employer Housing": "for free"
}

# ==============================================================================
# 4. SIDEBAR NAVIGATION
# ==============================================================================
with st.sidebar:
    st.markdown("""
        <div style="padding: 12px 0 16px 0;">
            <div style="font-family: 'Merriweather', serif; font-size: 20px; font-weight: 700; color: #00205B;">
                Apex Underwrite
            </div>
            <div style="font-size: 11px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">
                Executive Credit Intelligence
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 3px solid #C59B27; padding: 8px 12px; border-radius: 2px; margin-bottom: 16px;">
            <div style="font-size: 10px; font-weight: 700; color: #00205B; text-transform: uppercase;">System Operational</div>
            <div style="font-size: 12px; color: #334155; font-weight: 600;">Balanced Random Forest v1.2</div>
        </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "Executive Overview & Strategy",
            "Portfolio Exhibits (EDA)",
            "Credit Underwriting Engine"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
        <div style="font-size: 11px; color: #475569; line-height: 1.6;">
            <strong>Institutional Governance:</strong><br>
            • <strong>Jain (Deemed-to-be University)</strong><br>
            • CMS Business School | <strong>FBA-03</strong><br>
            • <strong>Akshit Singh</strong> (25MBAR0401)<br>
            • <strong>Vinay Tiwari</strong> (25MBAR0247)<br>
            • Course: MLBA – MBA Sem III
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# PAGE 1: EXECUTIVE OVERVIEW & STRATEGY
# ==============================================================================
if page == "Executive Overview & Strategy":
    st.markdown("""
        <div class="mckinsey-banner mckinsey-view">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h1>Executive Briefing: Retail Credit Risk & Decision Strategy</h1>
                    <p>Strategic framework for quantifying loan default probability and protecting Tier-1 bank capital.</p>
                </div>
                <div>
                    <span class="badge-gold">Strategic Memorandum</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 4 Executive Metric Tiles (McKinsey Style)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown("""
            <div class="exhibit-card">
                <div class="exhibit-header">Historical Cohort</div>
                <div class="exhibit-kpi-value">1,000</div>
                <div class="exhibit-kpi-desc">Validated loan accounts analyzed from German Credit dataset.</div>
            </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown("""
            <div class="exhibit-card">
                <div class="exhibit-header">Portfolio Default Base</div>
                <div class="exhibit-kpi-value">30.0%</div>
                <div class="exhibit-kpi-desc">300 accounts experienced contractual payment delinquency.</div>
            </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown("""
            <div class="exhibit-card">
                <div class="exhibit-header">Defaulter Interception</div>
                <div class="exhibit-kpi-value">71.7%</div>
                <div class="exhibit-kpi-desc">Recall capture rate on high-risk borrowers on test holdout.</div>
            </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown("""
            <div class="exhibit-card">
                <div class="exhibit-header">Triage Governance</div>
                <div class="exhibit-kpi-value">3 Tiers</div>
                <div class="exhibit-kpi-desc">Straight-through approval, secondary review, or decline.</div>
            </div>
        """, unsafe_allow_html=True)

    col_a, col_b = st.columns([1.6, 1.2])

    with col_a:
        st.markdown("### Strategic Dilemma: The Asymmetry of Lending Losses")
        st.markdown("""
        In retail credit underwriting, the cost of predictive classification errors is fundamentally asymmetric:
        
        * **Type II Error (False Negative — Capital Destruction):**  
          Approving a borrower who subsequently defaults. The bank absorbs a direct write-off of **100% of the principal loan amount** plus legal recovery fees ($5,000 to $10,000+ per occurrence).
          
        * **Type I Error (False Positive — Opportunity Margin Forfeiture):**  
          Rejecting a creditworthy applicant. The bank forfeits the net interest margin (typically 6% to 10%) and risks client relationship friction.
          
        **Strategic Directive:**  
        Because default write-offs erode Tier-1 regulatory capital reserves at a multiple of 10x to 15x relative to lost interest margin, the analytical pipeline is calibrated to prioritize **Recall on Defaulters (71.7%)** using balanced class penalty matrices.
        """)

    with col_b:
        st.markdown("### Institutional Policy Matrix")
        st.markdown("""
            <div class="exhibit-card">
                <div style="font-weight: 700; color: #16A34A; font-size: 13px; font-family: 'Inter', sans-serif;">
                    🟢 TIER 1: PRIME APPROVAL (P &lt; 35%)
                </div>
                <div style="font-size: 13px; color: #334155; margin-top: 4px;">
                    Straight-through automated processing. Prime base rate + 1.25% margin. Zero secondary collateral or guarantor required.
                </div>
            </div>

            <div class="exhibit-card">
                <div style="font-weight: 700; color: #D97706; font-size: 13px; font-family: 'Inter', sans-serif;">
                    🟡 TIER 2: CONDITIONAL REVIEW (35% &le; P &le; 55%)
                </div>
                <div style="font-size: 13px; color: #334155; margin-top: 4px;">
                    Heightened exposure zone. Counter-offer with shortened amortization (&lt; 18 months), require an employed co-signer, or add +275 bps risk spread.
                </div>
            </div>

            <div class="exhibit-card">
                <div style="font-weight: 700; color: #DC2626; font-size: 13px; font-family: 'Inter', sans-serif;">
                    🔴 TIER 3: PORTFOLIO DECLINE (P &gt; 55%)
                </div>
                <div style="font-size: 13px; color: #334155; margin-top: 4px;">
                    Actuarial default risk exceeds portfolio risk appetite. Adverse action notice issued or 100% liquid cash-collateralized structure required.
                </div>
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# PAGE 2: PORTFOLIO EXHIBITS (EDA)
# ==============================================================================
elif page == "Portfolio Exhibits (EDA)":
    st.markdown("""
        <div class="mckinsey-banner mckinsey-view">
            <h1>Portfolio Evidence & Solvency Indicators</h1>
            <p>Empirical findings from historical credit portfolios supporting risk-weighted modeling.</p>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "Exhibit 1: Checking Account Liquidity",
        "Exhibit 2: Loan Tenure Exposure",
        "Exhibit 3: Cohort Population Distribution"
    ])

    base_img_path = os.path.join(os.path.dirname(__file__), "images")

    with tab1:
        st.markdown("#### Exhibit 1: Checking Account Balance as the Primary Solvency Signal")
        c1, c2 = st.columns([1.3, 1])
        with c1:
            img1 = os.path.join(base_img_path, "fig2_checking_vs_default.png")
            if os.path.exists(img1):
                st.image(img1, use_container_width=True)
            else:
                st.info("Exhibit graphic available in repository.")
        with c2:
            st.markdown("""
                <div class="exhibit-card">
                    <div class="exhibit-header">Executive Takeaway</div>
                    <div style="font-size: 14px; line-height: 1.6; color: #1E293B;">
                        <strong>Key Empirical Observation:</strong><br>
                        • Borrowers with <strong>negative operating checking balances (&lt; 0 DM)</strong> experience default rates approaching <strong>49.3%</strong>.<br><br>
                        • Conversely, borrowers maintaining cash reserves of <strong>&ge; 200 DM</strong> show default rates below <strong>14.5%</strong>.<br><br>
                        <strong>Policy Directive:</strong><br>
                        Current account liquidity is the single most predictive early warning indicator of imminent personal default. Unsecured loan applications from overdrawn account holders should be declined outright or subjected to mandatory collateralization.
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("#### Exhibit 2: Impact of Amortization Horizon on Default Probability")
        c1, c2 = st.columns([1.3, 1])
        with c1:
            img2 = os.path.join(base_img_path, "fig3_duration_vs_risk.png")
            if os.path.exists(img2):
                st.image(img2, use_container_width=True)
            else:
                st.info("Exhibit graphic available in repository.")
        with c2:
            st.markdown("""
                <div class="exhibit-card">
                    <div class="exhibit-header">Tenure Risk Analysis</div>
                    <div style="font-size: 14px; line-height: 1.6; color: #1E293B;">
                        <strong>Key Empirical Observation:</strong><br>
                        • The median tenure of defaulting loan accounts is <strong>30 months</strong>, compared to <strong>18 months</strong> for fully performing accounts.<br><br>
                        • Over multi-year repayment horizons, macroeconomic fluctuations, job displacement, and personal health events compound default risk exponentially.<br><br>
                        <strong>Policy Directive:</strong><br>
                        For borderline applicants, senior underwriters should systematically counter-offer with compressed loan tenures (under 18–24 months) to contain life-cycle volatility.
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("#### Exhibit 3: Historical Training Population Class Structure")
        c1, c2 = st.columns([1.3, 1])
        with c1:
            img3 = os.path.join(base_img_path, "fig1_risk_distribution.png")
            if os.path.exists(img3):
                st.image(img3, use_container_width=True)
            else:
                st.info("Exhibit graphic available in repository.")
        with c2:
            st.markdown("""
                <div class="exhibit-card">
                    <div class="exhibit-header">Statistical Calibration</div>
                    <div style="font-size: 14px; line-height: 1.6; color: #1E293B;">
                        <strong>Cohort Composition:</strong><br>
                        • <strong>Performing Loans (Good):</strong> 700 applicants (70.0%)<br>
                        • <strong>Defaulting Loans (Bad):</strong> 300 applicants (30.0%)<br><br>
                        <strong>Modeling Implications:</strong><br>
                        Standard unweighted classification algorithms naturally favor the 70% majority class. Implementing <code>class_weight='balanced'</code> recalibrates loss penalties, ensuring the Random Forest actively seeks out high-risk patterns among the 30% defaulter subset.
                    </div>
                </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# PAGE 3: CREDIT UNDERWRITING ENGINE
# ==============================================================================
elif page == "Credit Underwriting Engine":
    st.markdown("""
        <div class="mckinsey-banner mckinsey-view">
            <h1>Point-of-Sale Underwriting Memorandum Engine</h1>
            <p>Input borrower underwriting parameters to generate an actuarial risk profile and credit committee directive.</p>
        </div>
    """, unsafe_allow_html=True)

    # Input Form organized into 3 McKinsey Structural Pillars
    with st.form("underwriting_memo_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<div class="form-section-title">Pillar 1: Cash Liquidity & Solvency</div>', unsafe_allow_html=True)
            
            checking_label = st.selectbox(
                "Checking Account Balance",
                options=list(CHECKING_MAP.keys()),
                index=1,
                help="Operating liquid reserves in active checking account."
            )
            
            savings_label = st.selectbox(
                "Savings & Deposit Buffer",
                options=list(SAVINGS_MAP.keys()),
                index=1,
                help="Total liquid savings available across deposits and money-market accounts."
            )

            housing_label = st.selectbox(
                "Residential Ownership Status",
                options=list(HOUSING_MAP.keys()),
                index=0,
                help="Legal ownership status of primary applicant residence."
            )

        with col2:
            st.markdown('<div class="form-section-title">Pillar 2: Loan Facility Terms</div>', unsafe_allow_html=True)
            
            credit_amount = st.slider(
                "Requested Principal Amount (DM)",
                min_value=250,
                max_value=15000,
                value=3200,
                step=250,
                format="%d DM",
                help="Total borrowing principal requested by the client."
            )
            
            duration = st.slider(
                "Amortization Tenure (Months)",
                min_value=6,
                max_value=60,
                value=24,
                step=2,
                format="%d Months",
                help="Requested loan repayment horizon in months."
            )

            purpose_label = st.selectbox(
                "Designated Facility Purpose",
                options=list(PURPOSE_MAP.keys()),
                index=0,
                help="Stated commercial or consumer objective for the borrowed funds."
            )

        with col3:
            st.markdown('<div class="form-section-title">Pillar 3: Employment & Demographics</div>', unsafe_allow_html=True)
            
            age = st.slider(
                "Borrower Age (Years)",
                min_value=18,
                max_value=75,
                value=34,
                format="%d Years",
                help="Chronological age of primary borrowing applicant."
            )

            employment_label = st.selectbox(
                "Employment Tenure (Current Role)",
                options=list(EMPLOYMENT_MAP.keys()),
                index=1,
                help="Continuous employment service with primary employer or enterprise."
            )

            st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("EVALUATE APPLICANT & GENERATE CREDIT MEMORANDUM", use_container_width=True)

    # Output Memorandum (McKinsey Style)
    if submitted:
        if model is None:
            st.error("Scoring pipeline (model.pkl) was not located. Please verify deployment path.")
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
            ref_id = f"MEMO-CR-{datetime.datetime.now().strftime('%Y%m%d')}-{abs(hash(str(credit_amount) + str(age))) % 10000:04d}"

            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            
            # Memorandum Header
            st.markdown(f"""
                <div style="background: #00205B; color: #FFFFFF; padding: 14px 22px; border-radius: 4px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-family: 'Merriweather', serif; font-size: 16px; font-weight: 700;">CREDIT COMMITTEE UNDERWRITING MEMORANDUM</div>
                        <div style="font-size: 12px; color: #CBD5E1; margin-top: 2px;">File Reference: {ref_id} | Issued: {datetime.datetime.now().strftime('%d-%b-%Y %H:%M UTC')}</div>
                    </div>
                    <div style="text-align: right;">
                        <span class="badge-gold">Facility: {credit_amount:,} DM ({duration} Mo)</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            res_left, res_right = st.columns([1.2, 1])

            with res_left:
                # Decision Recommendation
                if prob_default < 0.35:
                    st.markdown(f"""
                        <div class="verdict-approved">
                            <div style="font-family: 'Merriweather', serif; font-size: 17px; font-weight: 700; color: #16A34A;">
                                RECOMMENDATION: PRIME APPROVAL (STRAIGHT-THROUGH)
                            </div>
                            <div style="font-size: 13px; color: #1E293B; margin-top: 6px;">
                                Actuarial Default Probability: <strong>{prob_default:.1%}</strong> | High Solvency Profile
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown("""
                        <div class="exhibit-card">
                            <div class="exhibit-header">Actionable Underwriting Directives</div>
                            <div style="font-size: 13.5px; line-height: 1.65; color: #1E293B;">
                                • <strong>Disbursement Approval:</strong> Authorized for automated, straight-through capital disbursement.<br>
                                • <strong>Pricing Terms:</strong> Prime Base Rate + 1.25% credit spread.<br>
                                • <strong>Security Requirement:</strong> Unsecured credit facility; no personal guarantee or collateral encumbrance required.<br>
                                • <strong>Payment Mandate:</strong> Standard automated direct debit repayment covenant.
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                elif prob_default <= 0.55:
                    st.markdown(f"""
                        <div class="verdict-conditional">
                            <div style="font-family: 'Merriweather', serif; font-size: 17px; font-weight: 700; color: #D97706;">
                                RECOMMENDATION: CONDITIONAL APPROVAL / SECONDARY REVIEW
                            </div>
                            <div style="font-size: 13px; color: #1E293B; margin-top: 6px;">
                                Actuarial Default Probability: <strong>{prob_default:.1%}</strong> | Heightened Sensitivity Band
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown("""
                        <div class="exhibit-card">
                            <div class="exhibit-header">Counter-Offer & Restructuring Directives</div>
                            <div style="font-size: 13.5px; line-height: 1.65; color: #1E293B;">
                                • <strong>Disbursement Status:</strong> Suspended pending secondary credit officer approval.<br>
                                • <strong>Structural Adjustments:</strong>
                                  <br>&nbsp;&nbsp;1. Compress amortization tenure from <strong>""" + str(duration) + """ months</strong> to <strong>""" + str(max(12, int(duration * 0.7))) + """ months</strong>.
                                  <br>&nbsp;&nbsp;2. Require an employed co-signer or verifiable liquid guarantor.
                                  <br>&nbsp;&nbsp;3. Price with risk-adjusted spread (+275 bps margin over benchmark).
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                else:
                    st.markdown(f"""
                        <div class="verdict-declined">
                            <div style="font-family: 'Merriweather', serif; font-size: 17px; font-weight: 700; color: #DC2626;">
                                RECOMMENDATION: APPLICATION DECLINED (EXCEEDS RISK APPETITE)
                            </div>
                            <div style="font-size: 13px; color: #1E293B; margin-top: 6px;">
                                Actuarial Default Probability: <strong>{prob_default:.1%}</strong> | Subprime Risk Profile
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown("""
                        <div class="exhibit-card">
                            <div class="exhibit-header">Adverse Action & Alternative Restructuring Directives</div>
                            <div style="font-size: 13.5px; line-height: 1.65; color: #1E293B;">
                                • <strong>Disbursement Status:</strong> Declined under standard unsecured retail lending criteria.<br>
                                • <strong>Risk Rationale:</strong> The probability of 90-day delinquency exceeds institutional loss ceilings.<br>
                                • <strong>Alternative Pathway:</strong> Offer a 100% cash-collateralized structure (term deposit lien) to proceed.
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            with res_right:
                st.markdown("#### Exhibit 3A: Actuarial Probability Distribution")
                
                # McKinsey Style High-Readability Horizontal Bar Chart
                fig, ax = plt.subplots(figsize=(6.0, 2.6), dpi=140)
                fig.patch.set_facecolor('#FFFFFF')
                ax.set_facecolor('#FFFFFF')
                
                categories = ['Repayment\nConfidence', 'Default\nExposure']
                scores = [prob_good * 100, prob_default * 100]
                colors = ['#00205B', '#C59B27'] # McKinsey Navy & Ochre Gold
                
                bars = ax.barh(categories, scores, color=colors, height=0.45, edgecolor='none')
                ax.set_xlim(0, 118)
                ax.set_xlabel('Actuarial Probability Share (%)', fontsize=11, color='#00205B', fontweight='700', fontname='DejaVu Sans')
                ax.tick_params(colors='#0F172A', labelsize=11)
                
                # Direct readable data labels
                for bar in bars:
                    w = bar.get_width()
                    ax.text(w + 2.5, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', 
                            va='center', ha='left', fontweight='bold', color='#00205B', fontsize=12)
                
                # Minimalist spines & clean lines
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_color('#D1D5DB')
                ax.spines['bottom'].set_color('#D1D5DB')
                ax.grid(axis='x', linestyle='--', alpha=0.35, color='#94A3B8')
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

                # Detected Profile Drivers
                st.markdown("<div style='font-size: 11px; font-weight: 700; color: #00205B; letter-spacing: 0.05em; text-transform: uppercase; margin: 12px 0 6px 0;'>DETECTED PROFILE INFLUENCERS:</div>", unsafe_allow_html=True)

                if raw_checking == "<0":
                    st.markdown('<div class="factor-negative">[-] Overdrawn / Negative checking balance signals immediate cash flow vulnerability.</div>', unsafe_allow_html=True)
                elif raw_checking in [">=200", "no checking"]:
                    st.markdown('<div class="factor-positive">[+] Solid current account liquidity provides a resilient repayment buffer.</div>', unsafe_allow_html=True)

                if duration > 36:
                    st.markdown('<div class="factor-negative">[-] Extended tenure (>36 months) multiplies vulnerability to macroeconomic fluctuations.</div>', unsafe_allow_html=True)
                elif duration <= 18:
                    st.markdown('<div class="factor-positive">[+] Compact amortization horizon (≤18 months) minimizes default exposure.</div>', unsafe_allow_html=True)

                if raw_savings in [">=1000", "500<=X<1000"]:
                    st.markdown('<div class="factor-positive">[+] Substantial savings buffer acts as reliable safety net against unexpected shocks.</div>', unsafe_allow_html=True)
                elif raw_savings == "<100":
                    st.markdown('<div class="factor-negative">[-] Minimal emergency savings reserve leaves applicant sensitive to financial disruption.</div>', unsafe_allow_html=True)

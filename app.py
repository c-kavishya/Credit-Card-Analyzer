from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

st.set_page_config(page_title="Credit Card & Bank Statement Auditor", layout="wide")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemma-4-31b-it", temperature=0.2)

# CSS for dark-themed scrollable output containers
st.markdown("""
<style>
.scroll-box {
    height: 280px;
    overflow-y: auto;
    padding: 14px 18px;
    border: 1px solid #333;
    border-radius: 8px;
    background-color: #1e1e1e;
    font-size: 0.92rem;
    line-height: 1.6;
}
.scroll-box p, .scroll-box li {
    color: #e0e0e0;
}
</style>
""", unsafe_allow_html=True)

st.title("Credit Card Statement Auditor & Budget Planner")

left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("Account Statement Data")
    statement_input = st.text_area(
        label="Paste statement transactions below",
        height=480,
        placeholder="""Paste raw transaction rows or CSV exports here, for example:
08/12 Netflix Subscription $15.99
08/14 Uber Eats $42.50
08/15 Gym Auto-Renew $55.00
08/16 Late Payment Fee $39.00
08/18 DoorDash $38.20
08/20 Annual Card Fee $95.00""",
        label_visibility="collapsed"
    )
    analyze_btn = st.button("Audit Statement", type="primary", use_container_width=True)

with right_col:
    st.subheader("Financial Leak & Anomaly Report")
    audit_box = st.empty()
    audit_box.markdown('<div class="scroll-box">Awaiting statement data...</div>', unsafe_allow_html=True)

    st.subheader("Subscription Cut List & 50/30/20 Plan")
    plan_box = st.empty()
    plan_box.markdown('<div class="scroll-box">Awaiting audit completion...</div>', unsafe_allow_html=True)

if analyze_btn:
    if not statement_input.strip():
        st.warning("Please paste at least one month of transaction data.")
    else:
        with st.spinner("Auditing transactions and categorizing expenses..."):
            
            # ── STAGE 1: Extract, Categorize & Flag Anomalies ──
            stage1_prompt = f"""
You are a certified forensic financial auditor.

Analyze the statement transactions below. For every transaction, extract:
1. Date (if present)
2. Merchant / Description
3. Estimated Category (Essentials, Dining/Discretionary, Subscriptions, Bank Fees)
4. Amount
5. Risk / Leak Tag:
   - FLAG AS 'DORMANT_LEAK' if it looks like a recurring subscription or fitness club.
   - FLAG AS 'SURGE' if it is an unusually high discretionary or dining expense.
   - FLAG AS 'FEE_PENALTY' for late fees, overdrafts, interest charges, or card maintenance fees.
   - Otherwise mark as 'NORMAL'.

Format your response as a clean bullet list:
- [Category] Merchant: $Amount | Tag: DORMANT_LEAK / SURGE / FEE_PENALTY / NORMAL | Notes

Statement Data:
{statement_input}
"""
            stage1_res = llm.invoke(stage1_prompt)
            extracted_audit = stage1_res.text

            # ── STAGE 2: Advisory, Cut-List & Budget Plan ──
            stage2_prompt = f"""
You are an expert personal financial advisor and debt counselor.

Based on the flagged audit below, generate two clearly designated sections:

SECTION 1 - FINANCIAL HEALTH DIAGNOSIS:
Provide a 4-5 line assessment explaining the user's biggest spending leaks, 
the total estimated waste on avoidable fees/subscriptions, and overall financial risk.

SECTION 2 - CUT-LIST & RESTRUCTURING PLAN:
1. Immediate Cut-List: Name specific subscriptions or repeated fees that should be canceled or disputed immediately.
2. 50/30/20 Action Target: Briefly indicate what adjustments are required to align their cash flow with 50% Needs, 30% Wants, and 20% Savings/Debt Repayment.

Flagged Audit Data:
{extracted_audit}
"""
            stage2_res = llm.invoke(stage2_prompt)
            full_plan = stage2_res.text

        # Separate Section 1 and Section 2 for targeted UI display
        if "SECTION 2" in full_plan:
            parts = full_plan.split("SECTION 2")
            diagnosis = parts[0].replace("SECTION 1 - FINANCIAL HEALTH DIAGNOSIS:", "").replace("SECTION 1", "").strip()
            action_plan = ("SECTION 2" + parts[1]).replace("SECTION 2 - CUT-LIST & RESTRUCTURING PLAN:", "").replace("SECTION 2", "").strip()
        else:
            diagnosis = full_plan
            action_plan = "See diagnostic summary above."

        # Render to scrollable cards
        audit_box.markdown(
            f'<div class="scroll-box">{extracted_audit}</div>',
            unsafe_allow_html=True
        )
        plan_box.markdown(
            f'<div class="scroll-box"><strong>Diagnosis:</strong><br>{diagnosis}<br><br><strong>Action Plan:</strong><br>{action_plan}</div>',
            unsafe_allow_html=True
        )
"""
Streamlit Chatbot UI for Loan Approval System
User-friendly interface for submitting loan applications and viewing results.
"""

import streamlit as st
import requests
import json
from datetime import datetime

# Configure Streamlit
st.set_page_config(
    page_title="Loan Approval System",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API endpoint
API_URL = "http://localhost:8000"

st.title("💳 Intelligent Loan Approval System")
st.markdown("---")

# Sidebar for navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["Apply for a Loan", "Check Application Status", "Compliance Dashboard"]
)

# ============================================
# PAGE 1: Apply for a Loan
# ============================================
if page == "Apply for a Loan":
    st.header("Submit Your Loan Application")

    # Application Details Section
    st.subheader("📋 Applicant Information")

    st.info("ℹ️ **Sample Applicants Available:**\n- **APP001**: Strong applicant (High income, Excellent credit)\n- **APP002**: Medium risk (Moderate income, Fair credit)\n- **APP003**: Very strong applicant (High income, Excellent credit)")

    col1, col2, col3 = st.columns(3)

    with col1:
        applicant_id = st.selectbox(
            "Select Applicant ID",
            ["APP001", "APP002", "APP003"],
            index=0,
            help="Choose from available sample applicants"
        )
    with col2:
        age = st.number_input(
            "Age (years)",
            min_value=18,
            max_value=100,
            value=35,
            step=1
        )
    with col3:
        contact_email = st.text_input(
            "Contact Email",
            placeholder="your.email@example.com"
        )

    # Financial Details Section
    st.subheader("💰 Financial Information")
    col1, col2, col3 = st.columns(3)

    with col1:
        annual_income = st.number_input(
            "Annual Income ($)",
            min_value=10000,
            max_value=5000000,
            value=75000,
            step=5000,
            help="Your yearly income"
        )
    with col2:
        credit_score = st.number_input(
            "Credit Score",
            min_value=300,
            max_value=900,
            value=750,
            step=10,
            help="Credit score (300-900)"
        )
    with col3:
        existing_liabilities = st.number_input(
            "Existing Monthly Liabilities ($)",
            min_value=0,
            max_value=500000,
            value=2000,
            step=100,
            help="Monthly debt obligations"
        )

    # Employment Details Section
    st.subheader("🏢 Employment Information")
    col1, col2, col3 = st.columns(3)

    with col1:
        employment_type = st.selectbox(
            "Employment Type",
            ["Full-time", "Contract", "Self-employed", "Part-time"],
            index=0,
            help="Your employment status"
        )
    with col2:
        employment_years = st.number_input(
            "Years in Current Employment",
            min_value=0,
            max_value=60,
            value=8,
            step=1,
            help="How long in current job"
        )
    with col3:
        location = st.text_input(
            "Location",
            placeholder="City, State",
            help="Your location"
        )

    # Loan Details Section
    st.subheader("🏦 Loan Request")
    col1, col2 = st.columns(2)

    with col1:
        loan_amount = st.number_input(
            "Loan Amount ($)",
            min_value=1000,
            max_value=1000000,
            value=50000,
            step=5000,
            help="Amount you want to borrow"
        )

    with col2:
        tenure_months = st.number_input(
            "Loan Tenure (months)",
            min_value=6,
            max_value=360,
            value=60,
            step=6,
            help="How long to repay the loan"
        )

    st.markdown("---")

    if st.button("Submit Application", use_container_width=True, type="primary"):
        if not applicant_id:
            st.error("❌ Please enter an Applicant ID")
        else:
            with st.spinner("🔄 Processing your application..."):
                try:
                    # Send request to FastAPI backend
                    response = requests.post(
                        f"{API_URL}/apply",
                        json={
                            "applicant_id": applicant_id,
                            "age": age,
                            "annual_income": annual_income,
                            "credit_score": credit_score,
                            "existing_liabilities": existing_liabilities,
                            "employment_type": employment_type,
                            "employment_years": employment_years,
                            "location": location if location else "Not provided",
                            "loan_amount": loan_amount,
                            "tenure_months": tenure_months,
                            "contact_email": contact_email if contact_email else None
                        },
                        timeout=30
                    )

                    if response.status_code == 200:
                        result = response.json()

                        # Display results
                        st.success("✅ Application Processed Successfully!")

                        # Decision Display with Color Coding
                        decision = result['decision']
                        confidence = result['confidence']

                        if decision == "Approved":
                            st.balloons()
                            with st.container(border=True):
                                st.markdown("<h2 style='text-align: center; color: green;'>✅ APPROVED</h2>", unsafe_allow_html=True)
                                st.markdown(f"<p style='text-align: center; font-size: 18px;'>Your loan application has been <b>APPROVED</b></p>", unsafe_allow_html=True)
                        elif decision == "Rejected":
                            with st.container(border=True):
                                st.markdown("<h2 style='text-align: center; color: red;'>❌ REJECTED</h2>", unsafe_allow_html=True)
                                st.markdown(f"<p style='text-align: center; font-size: 18px;'>Your loan application has been <b>REJECTED</b></p>", unsafe_allow_html=True)
                        else:  # Review
                            with st.container(border=True):
                                st.markdown("<h2 style='text-align: center; color: orange;'>🟡 UNDER REVIEW</h2>", unsafe_allow_html=True)
                                st.markdown(f"<p style='text-align: center; font-size: 18px;'>Your loan application is <b>UNDER REVIEW</b></p>", unsafe_allow_html=True)
                                st.markdown("<p style='text-align: center; font-size: 14px;'>Our team will review your application and get back to you within 2-3 business days.</p>", unsafe_allow_html=True)

                        # Key Metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Decision Status", decision)

                        with col2:
                            st.metric("Confidence Level", f"{confidence:.1%}")

                        with col3:
                            st.metric("Risk Assessment", result['risk_level'])

                        st.markdown("---")

                        st.subheader("📋 Decision Details")
                        st.info(f"**Case ID:** {result['case_id']}")

                        st.write("**Explanation:**")
                        st.write(result['explanation'])

                        st.write("**Key Factors:**")
                        for factor in result['factors']:
                            if "⚠️" in factor:
                                st.warning(factor)
                            else:
                                st.write(f"✓ {factor}")

                        # Store in session state for status check
                        st.session_state.last_case_id = result['case_id']
                        st.session_state.last_applicant_id = applicant_id

                    else:
                        error_detail = response.json().get("detail", "Unknown error")
                        st.error(f"❌ Error: {error_detail}")

                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to the backend server. Make sure the FastAPI service is running on localhost:8000")
                except requests.exceptions.Timeout:
                    st.error("❌ Request timed out. The backend server might be slow or unresponsive.")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")

# ============================================
# PAGE 2: Check Application Status
# ============================================
elif page == "Check Application Status":
    st.header("Check Your Application Status")

    applicant_id = st.text_input(
        "Enter Applicant ID",
        placeholder="APP001"
    )

    if st.button("Check Status", use_container_width=True):
        if not applicant_id:
            st.error("❌ Please enter an Applicant ID")
        else:
            with st.spinner("🔄 Fetching application status..."):
                try:
                    response = requests.get(
                        f"{API_URL}/status/{applicant_id}",
                        timeout=10
                    )

                    if response.status_code == 200:
                        status = response.json()

                        st.success("✅ Application Found!")

                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Applicant ID:** {status.get('applicant_id')}")
                            st.write(f"**Case ID:** {status.get('case_id')}")

                        with col2:
                            st.write(f"**Status:** {status.get('status')}")
                            st.write(f"**Timestamp:** {status.get('timestamp', 'N/A')}")

                        if "decision" in status:
                            decision_color = {
                                "Approved": "🟢",
                                "Rejected": "🔴",
                                "Review": "🟡"
                            }
                            st.info(f"{decision_color.get(status['decision'], '⚪')} **Decision:** {status['decision']}")

                    elif response.status_code == 404:
                        st.warning("⚠️ Application not found")
                    else:
                        st.error(f"❌ Error: {response.json().get('detail')}")

                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to the backend server.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ============================================
# PAGE 3: Compliance Dashboard
# ============================================
elif page == "Compliance Dashboard":
    st.header("📊 Compliance Dashboard")

    if st.button("Refresh Data", use_container_width=True):
        st.rerun()

    with st.spinner("🔄 Loading compliance data..."):
        try:
            response = requests.get(
                f"{API_URL}/compliance-summary",
                timeout=10
            )

            if response.status_code == 200:
                summary = response.json()

                # Key metrics
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Total Cases", summary['total_cases'])

                with col2:
                    st.metric("Approvals", summary['approvals'], delta=f"{summary.get('approval_rate', 0):.1f}%")

                with col3:
                    st.metric("Rejections", summary['rejections'])

                with col4:
                    st.metric("Under Review", summary['reviews'])

                st.markdown("---")

                # Recent applications
                st.subheader("📝 Recent Applications")

                if summary['logs']:
                    for log in reversed(summary['logs'][-10:]):
                        with st.expander(f"Case: {log.get('case_id', 'N/A')} - {log.get('applicant_id', 'N/A')}"):
                            col1, col2, col3 = st.columns(3)

                            with col1:
                                decision = log.get('decision', 'N/A')
                                decision_color = {
                                    "Approved": "🟢",
                                    "Rejected": "🔴",
                                    "Review": "🟡"
                                }
                                st.write(f"**Decision:** {decision_color.get(decision, '⚪')} {decision}")

                            with col2:
                                st.write(f"**Risk Level:** {log.get('risk_level', 'N/A')}")

                            with col3:
                                st.write(f"**Status:** {log.get('status', 'N/A')}")

                            if "explanation" in log:
                                st.write(f"**Details:** {log['explanation']}")
                else:
                    st.info("ℹ️ No applications processed yet")

            else:
                st.error("❌ Error fetching compliance data")

        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to the backend server.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Sidebar information
st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 How to Use")
st.sidebar.markdown("""
1. **Apply for a Loan**: Submit your application with your ID and loan details
2. **Check Status**: Look up your application status by Applicant ID
3. **Compliance Dashboard**: View system-wide statistics and recent cases

### ℹ️ Sample IDs
- APP001 (Strong applicant)
- APP002 (Medium risk)
- APP003 (Very strong applicant)

### ⚙️ Backend Status
Check if API is running: [Health Check](http://localhost:8000/health)
""")

st.sidebar.markdown("---")
st.sidebar.caption("Agentic AI Loan Approval System v1.0")

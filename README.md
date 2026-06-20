# 💳 Agentic AI Intelligent Loan Approval System

A complete multi-agent AI system for automated loan application analysis using FastMCP, LangGraph, and Claude AI.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Streamlit Chatbot UI (Frontend)                │
│   - Loan application form                                   │
│   - Status checking                                         │
│   - Compliance dashboard                                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│         FastAPI Microservice (Orchestration)               │
│   - Main /apply endpoint                                   │
│   - Coordinates all agents                                 │
│   - Returns unified response                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┬────────────────┐
         ▼             ▼             ▼                ▼
    ┌────────────┐ ┌────────────┐ ┌────────┐    ┌────────────┐
    │Applicant   │ │Financial   │ │Decision│    │Compliance  │
    │Profile     │ │Risk        │ │Agent   │    │Agent       │
    │Agent       │ │Agent       │ │        │    │            │
    │(MCP)       │ │(MCP)       │ │(MCP)   │    │(MCP)       │
    └────────────┘ └────────────┘ └────────┘    └────────────┘
         ▲             ▲             ▲                ▲
         └─────────────┴─────────────┴────────────────┘
                  Uses Claude API
```

## 📁 Project Structure

```
loan_approval_system/
├── main.py                      # FastAPI microservice
├── app.py                       # Streamlit UI
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── agents/
│   ├── __init__.py
│   ├── decision_agent.py        # Loan decision logic
│   └── compliance_agent.py      # Compliance & notifications
├── mcp_servers/
│   ├── __init__.py
│   ├── applicant_agent.py       # Applicant profile analysis
│   └── risk_agent.py            # Financial risk analysis
└── utils/
    ├── __init__.py
    └── claude_client.py         # Claude API integration
```

## 🚀 Quick Start

### Step 1: Set Up Environment

```bash
cd loan_approval_system

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Key

```bash
# Edit .env file and add your Anthropic API key
nano .env
# Or open in your editor and set:
# ANTHROPIC_API_KEY=your_actual_api_key_here
```

### Step 3: Start the Backend (FastAPI)

In one terminal:

```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 4: Start the Frontend (Streamlit)

In another terminal:

```bash
streamlit run app.py
```

This will open automatically at `http://localhost:8501`

### Step 5: Test the System

1. Go to **Apply for a Loan**
2. Enter an Applicant ID: `APP001`, `APP002`, or `APP003`
3. Fill in loan amount and tenure
4. Click "Submit Application"
5. View the decision!

## 📚 How It Works

### Workflow Overview

When you submit a loan application, here's what happens:

1. **Application Submitted** → FastAPI `/apply` endpoint receives the request

2. **Applicant Profile Analysis** → Applicant Agent:
   - Fetches applicant profile from mock database
   - Calculates income stability score
   - Assesses employment risk
   - Summarizes credit history

3. **Financial Risk Analysis** → Risk Agent:
   - Calculates debt-to-income ratio
   - Assesses credit risk level
   - Analyzes loan-to-income ratio
   - Detects anomalies/red flags

4. **Decision Making** → Decision Agent:
   - Scores the application (0-5 points)
   - Determines decision: Approved/Rejected/Review
   - Generates explanation using Claude AI
   - Calculates confidence level

5. **Compliance & Logging** → Compliance Agent:
   - Creates case record
   - Logs decision for audit trail
   - Sends notification
   - Updates compliance dashboard

6. **Response Returned** → Result shown in UI

## 🧪 Sample Test Cases

### Test Case 1: Strong Applicant (APP001)
- Income: $75,000
- Credit Score: 750
- Employment: Full-time, 8 years
- **Expected Result**: ✅ Approved

### Test Case 2: Medium Risk (APP002)
- Income: $45,000
- Credit Score: 620
- Employment: Contract, 2 years
- **Expected Result**: 🟡 Review

### Test Case 3: Very Strong (APP003)
- Income: $120,000
- Credit Score: 800
- Employment: Full-time, 15 years
- **Expected Result**: ✅ Approved

## 🔧 Key Components Explained

### 1. Applicant Profile Agent (`mcp_servers/applicant_agent.py`)
**MCP Server**: ApplicantProfileAgent

**Tools**:
- `fetch_applicant_profile(applicant_id)` - Get applicant data
- `calculate_income_stability_score()` - Score income stability
- `get_employment_risk()` - Assess employment risk
- `get_credit_history_summary()` - Summarize credit profile

### 2. Financial Risk Agent (`mcp_servers/risk_agent.py`)
**MCP Server**: FinancialRiskAnalysisAgent

**Tools**:
- `calculate_debt_to_income_ratio()` - Calculate DTI
- `get_credit_risk_level()` - Score credit risk
- `analyze_loan_amount_risk()` - Check loan appropriateness
- `detect_anomalies()` - Find red flags
- `generate_risk_summary()` - Summarize overall risk

### 3. Decision Agent (`agents/decision_agent.py`)
**MCP Server**: LoanDecisionAgent

**Tools**:
- `make_loan_decision()` - Make final decision with reasoning

**Scoring Logic**:
- Income Stability: +1 if score > 0.7
- Credit Risk: +1 if "Low"
- DTI Ratio: +1 if < 0.4
- Employment: +1 if "Low" risk
- Loan-to-Income: +1 if ≤ 2x income

Decision thresholds:
- **≥4 points**: Approved (95% confidence)
- **2.5-3.9 points**: Review (75% confidence)
- **<2.5 points**: Rejected (90% confidence)

### 4. Compliance Agent (`agents/compliance_agent.py`)
**MCP Server**: ComplianceOrchestratorAgent

**Tools**:
- `log_decision()` - Audit log entry
- `send_notification()` - Send decision to applicant
- `create_case_record()` - Case management
- `get_compliance_summary()` - Dashboard stats

### 5. FastAPI Microservice (`main.py`)
**Main Endpoints**:

```
POST /apply
- Input: Applicant ID, Loan Amount, Tenure, Email
- Output: Decision, Factors, Explanation, Case ID

GET /health
- Checks if API is running

GET /compliance-summary
- Returns statistics and recent cases

GET /status/{applicant_id}
- Retrieves application status
```

## 🎨 Streamlit UI (`app.py`)

### Three Pages

1. **Apply for a Loan**
   - Form to submit applications
   - Real-time decision display
   - Factor breakdown
   - AI-generated explanation

2. **Check Application Status**
   - Look up any application by ID
   - View decision and details

3. **Compliance Dashboard**
   - System-wide statistics
   - Approval/rejection rates
   - Recent cases
   - Risk levels

## 💡 Understanding the Claude Integration

The system uses Claude AI in two places:

### 1. Decision Explanation
When a decision is made, Claude generates a human-friendly explanation. Example:
```
Decision: Approved
Explanation: "Your application has been approved based on your strong income 
stability, good credit profile, and healthy debt-to-income ratio. We're pleased 
to move forward with processing your loan."
```

### 2. Using the Claude API
In `utils/claude_client.py`:
```python
client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    messages=[{"role": "user", "content": prompt}]
)
```

## 🔍 Debugging & Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# If in use, kill the process or use different port
# In main.py, change: uvicorn.run(app, port=8001)
```

### Streamlit won't connect to backend
```
Error: "Cannot connect to the backend server"

Solution:
1. Make sure FastAPI is running on localhost:8000
2. Check firewall settings
3. Try accessing http://localhost:8000/health in browser
```

### Claude API errors
```
Error: "API key not found"

Solution:
1. Check .env file has ANTHROPIC_API_KEY set
2. Verify API key is valid
3. Check you have API credits
```

### Application ID not found
```
Error: "Applicant {applicant_id} not found"

Solution:
Use sample IDs: APP001, APP002, or APP003
To add more, edit MOCK_APPLICANTS in mcp_servers/applicant_agent.py
```

## 📈 Next Steps & Enhancements

1. **Real Database**: Replace mock data with actual database
2. **LangGraph**: Implement proper orchestration with LangGraph workflows
3. **User Authentication**: Add login/security
4. **More Agents**: Add Fraud Detection, Income Verification agents
5. **Testing**: Add pytest test suite
6. **Deployment**: Docker containerization and cloud deployment
7. **Monitoring**: Add logging, metrics, and alerting

## 📝 Learning Objectives Covered

✅ Multi-agent architecture design
✅ MCP (Model Context Protocol) integration
✅ FastAPI for microservices
✅ Streamlit for UI
✅ Claude AI integration
✅ Agent orchestration
✅ Decision-making workflows
✅ Compliance & audit logging

## 📚 Resources

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

## 🤝 Support

Need help?
1. Check the troubleshooting section above
2. Review code comments in each agent
3. Check API logs for errors
4. Verify sample data in mock databases

Happy coding! 🎉

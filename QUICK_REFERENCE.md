# ⚡ Quick Reference Guide

## 🚀 Quick Start (Copy & Paste)

```bash
# Terminal 1 - Start Backend
cd loan_approval_system
source venv/bin/activate
python main.py

# Terminal 2 - Start Frontend
cd loan_approval_system
source venv/bin/activate
streamlit run app.py
```

Then open: http://localhost:8501

---

## 🧪 Test with Sample Data

### Sample Applicants
| ID | Income | Credit | Employment | Result |
|---|---|---|---|---|
| APP001 | $75K | 750 | FT, 8yr | ✅ Approved |
| APP002 | $45K | 620 | Contract, 2yr | 🟡 Review |
| APP003 | $120K | 800 | FT, 15yr | ✅ Approved |

---

## 📊 API Endpoints

### Apply for Loan
```bash
curl -X POST http://localhost:8000/apply \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "APP001",
    "loan_amount": 50000,
    "tenure_months": 60,
    "contact_email": "test@example.com"
  }'
```

### Health Check
```bash
curl http://localhost:8000/health
```

### Compliance Summary
```bash
curl http://localhost:8000/compliance-summary
```

### Get Application Status
```bash
curl http://localhost:8000/status/APP001
```

---

## 🏛️ Architecture at a Glance

```
User (Streamlit UI)
  ↓ /apply request
FastAPI (main.py)
  ├→ Applicant Agent (fetch profile)
  ├→ Risk Agent (analyze finances)
  ├→ Decision Agent (decide + Claude explanation)
  └→ Compliance Agent (log & notify)
  ↓ response
Streamlit UI shows result
```

---

## 🎯 Decision Scoring System

**Points Awarded:**
- Income Stability > 0.7: +1
- Credit Risk = "Low": +1
- DTI Ratio < 0.4: +1
- Employment Risk = "Low": +1
- Loan-to-Income ≤ 2x: +1

**Score → Decision:**
- ≥ 4 points: ✅ **Approved** (95% confidence)
- 2.5-3.9 points: 🟡 **Review** (75% confidence)
- < 2.5 points: ❌ **Rejected** (90% confidence)

---

## 📁 File Map

```
main.py
  ↓ orchestrates
  ├→ mcp_servers/applicant_agent.py (profile analysis)
  ├→ mcp_servers/risk_agent.py (financial metrics)
  ├→ agents/decision_agent.py (decision logic + Claude)
  └→ agents/compliance_agent.py (logging)

app.py
  ↓ frontend UI calling
  └→ main.py (API backend)

utils/claude_client.py
  ↓ used by agents to generate explanations
```

---

## 🔧 Common Customizations

### Change Decision Rules
Edit `agents/decision_agent.py`, function `make_loan_decision()`

### Add New Applicant
Edit `mcp_servers/applicant_agent.py`, add to `MOCK_APPLICANTS`:
```python
"APP004": {
    "age": 40,
    "income": 90000,
    "employment_type": "Full-time",
    "credit_score": 700,
    "existing_liabilities": 3000,
    "employment_years": 10
}
```

### Change Claude Prompt
Edit `utils/claude_client.py`, modify the prompt in `generate_explanation()`

### Modify UI Layout
Edit `app.py`, sections under `if page == "Apply for a Loan":`

---

## 🐛 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Backend won't start | Check port 8000: `lsof -i :8000` |
| No module errors | Run: `pip install -r requirements.txt` |
| API key not found | Check `.env` file has key |
| Applicant not found | Use: APP001, APP002, or APP003 |
| Can't connect to backend | Check FastAPI running on 8000 |
| Streamlit won't load | Try: `streamlit run app.py --logger.level=debug` |

---

## 📚 Agent Reference

### Applicant Profile Agent
**Purpose**: Analyze applicant credentials
**Key Functions**:
- `fetch_applicant_profile()` - Get user data
- `calculate_income_stability_score()` - Score stability
- `get_employment_risk()` - Risk assessment
- `get_credit_history_summary()` - Credit summary

### Financial Risk Agent
**Purpose**: Analyze financial metrics
**Key Functions**:
- `calculate_debt_to_income_ratio()` - DTI calculation
- `get_credit_risk_level()` - Credit scoring
- `analyze_loan_amount_risk()` - Loan appropriateness
- `detect_anomalies()` - Red flags
- `generate_risk_summary()` - Risk overview

### Decision Agent
**Purpose**: Make final decision
**Key Functions**:
- `make_loan_decision()` - Decision + explanation

### Compliance Agent
**Purpose**: Log & notify
**Key Functions**:
- `log_decision()` - Audit log
- `send_notification()` - Email notification
- `create_case_record()` - Case tracking
- `get_compliance_summary()` - Statistics

---

## 🎓 Learning Path

1. ✅ Get it running (GETTING_STARTED.md)
2. ✅ Understand architecture (README.md)
3. ✅ Read code in agents (each agent file)
4. ✅ Modify decision rules
5. ✅ Add new agents
6. ✅ Connect to real database

---

## 💡 Tips for Development

1. **Use print() statements** to debug in FastAPI:
   ```python
   print(f"DTI: {dti_ratio}")  # Check terminal
   ```

2. **Use Streamlit.write()** to debug in UI:
   ```python
   st.write(f"Debug: {variable}")
   ```

3. **Check browser console** for frontend errors (F12)

4. **Check FastAPI logs** in terminal for backend errors

5. **Use curl** to test API without UI:
   ```bash
   curl http://localhost:8000/compliance-summary | python -m json.tool
   ```

---

## 🔗 Useful Links

- API Docs: http://localhost:8000/docs
- Streamlit App: http://localhost:8501
- Backend Health: http://localhost:8000/health
- Anthropic Console: https://console.anthropic.com/
- FastAPI Docs: https://fastapi.tiangolo.com/
- Streamlit Docs: https://docs.streamlit.io/

---

## 📝 Environment Variables

```env
# .env file
ANTHROPIC_API_KEY=your_key_here
```

---

## ⏱️ Typical Flow Times

- Submit application → Backend processing: **2-5 seconds**
- Claude explanation generation: **1-2 seconds**
- Total E2E time: **3-7 seconds**

---

## 🎯 Success Checklist

- [ ] Backend running (port 8000)
- [ ] Streamlit running (port 8501)
- [ ] Can submit APP001
- [ ] Get "Approved" decision
- [ ] See explanation text
- [ ] Factors displayed
- [ ] Dashboard shows 1+ case

---

## 🚀 Production Notes

Before deploying:
- [ ] Replace mock database with real DB
- [ ] Add proper authentication
- [ ] Use environment variables for config
- [ ] Add error handling
- [ ] Add logging/monitoring
- [ ] Use Docker for deployment
- [ ] Set up CI/CD pipeline
- [ ] Add comprehensive tests

---

**Need help?** Read the full README.md or GETTING_STARTED.md

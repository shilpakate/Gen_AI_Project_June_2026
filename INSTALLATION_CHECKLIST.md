# ✅ Installation & Setup Checklist

## Pre-Installation

- [ ] Python 3.9+ installed (`python --version`)
- [ ] pip installed (`pip --version`)
- [ ] Anthropic API key obtained from https://console.anthropic.com/
- [ ] Internet connection available

## Step 1: Environment Setup

- [ ] Navigate to project: `cd loan_approval_system`
- [ ] Create virtual env: `python3 -m venv venv`
- [ ] Activate venv: `source venv/bin/activate` (or Windows: `venv\Scripts\activate`)
- [ ] Verify activated: `which python` should show venv path

## Step 2: Dependencies Installation

- [ ] Run: `pip install -r requirements.txt`
- [ ] Verify: `pip list` shows all packages
- [ ] Check: `python -c "import fastapi; import streamlit; import anthropic"`

## Step 3: Configuration

- [ ] Open `.env` file
- [ ] Add API key: `ANTHROPIC_API_KEY=your_key_here`
- [ ] Save file
- [ ] Verify: `cat .env` shows key (DO NOT commit!)

## Step 4: Backend Testing

- [ ] Start backend: `python main.py`
- [ ] See: "Uvicorn running on http://0.0.0.0:8000"
- [ ] Open new terminal (keep backend running)
- [ ] Test health: `curl http://localhost:8000/health`
- [ ] See: `{"status":"healthy","service":"Loan Approval System"}`

## Step 5: Frontend Testing

- [ ] In new terminal, activate venv again
- [ ] Run: `streamlit run app.py`
- [ ] See: Browser opens at http://localhost:8501
- [ ] See: "Apply for a Loan" page loads

## Step 6: Full System Test

- [ ] Streamlit open in browser
- [ ] Enter Applicant ID: `APP001`
- [ ] Enter Loan Amount: `50000`
- [ ] Enter Tenure: `60`
- [ ] Click "Submit Application"
- [ ] Wait 3-7 seconds
- [ ] See: ✅ APPROVED decision
- [ ] See: Confidence score
- [ ] See: Claude explanation
- [ ] See: List of factors

## Step 7: Other Pages Testing

- [ ] Click "Check Application Status"
- [ ] Enter: `APP001`
- [ ] Click "Check Status"
- [ ] See: Application details

- [ ] Click "Compliance Dashboard"
- [ ] See: Statistics (1+ total cases)
- [ ] See: Application in recent list
- [ ] Click "Refresh Data"

## Step 8: Try More Test Cases

- [ ] Test APP002 (medium risk)
- [ ] Test APP003 (strong applicant)
- [ ] Try different loan amounts
- [ ] Try different tenures

## Troubleshooting Checks

### If Backend Won't Start
- [ ] Port 8000 free: `lsof -i :8000`
- [ ] Python version: `python --version` (3.9+)
- [ ] Dependencies: `pip list` shows fastapi
- [ ] API key: Check `.env` is readable

### If Frontend Won't Load
- [ ] Streamlit version: `streamlit --version`
- [ ] Backend running: Check other terminal
- [ ] Port 8501 free: `lsof -i :8501`
- [ ] Clear cache: `streamlit cache clear`

### If Getting API Errors
- [ ] API key valid: Try in console.anthropic.com
- [ ] API key in .env: Check exact location
- [ ] Backend logs: Check terminal for errors
- [ ] Rate limit: Check Anthropic dashboard

### If Getting "Module Not Found"
- [ ] Venv activated: `which python` shows venv
- [ ] Reinstall: `pip install -r requirements.txt --force-reinstall`
- [ ] Check: `pip list | grep fastapi` etc

## Post-Installation

- [ ] Documentation read: README.md
- [ ] Quick reference: QUICK_REFERENCE.md
- [ ] System overview: SYSTEM_OVERVIEW.md
- [ ] Getting started: GETTING_STARTED.md

## Performance Benchmarks

- [ ] Response time: 3-7 seconds
- [ ] CPU usage: Normal (20-40% during processing)
- [ ] Memory usage: <200MB
- [ ] No errors in terminal logs

## Security Checklist

- [ ] `.env` NOT in version control
- [ ] API key NOT in code files
- [ ] No hardcoded credentials
- [ ] CORS enabled for development only
- [ ] SQL injection: N/A (using Pydantic)
- [ ] XSS protection: Streamlit handles

## Ready to Go! 🎉

- [ ] All tests passed
- [ ] No errors in logs
- [ ] System responding normally
- [ ] Ready for development!

## Next Steps

1. **Understand the code**: Read each agent file
2. **Modify decision rules**: Edit `agents/decision_agent.py`
3. **Add new applicants**: Edit `MOCK_APPLICANTS`
4. **Customize prompts**: Edit `utils/claude_client.py`
5. **Connect real database**: Replace mock data
6. **Deploy**: Use Docker for production

---

**Total Setup Time**: ~15-20 minutes
**Difficulty**: Beginner-friendly ✓

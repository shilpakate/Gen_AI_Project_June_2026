#!/bin/bash

# Complete GitHub Push Script
# Run this on your LOCAL machine to push code to GitHub

set -e  # Exit on error

echo "================================================================================"
echo "🚀 PUSHING AGENTIC AI LOAN APPROVAL SYSTEM TO GITHUB"
echo "================================================================================"
echo ""
echo "Repository: https://github.com/shilpakate/Gen_AI_Project_June_2026"
echo "Username: shilpakate"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Verify git
echo -e "${BLUE}[1/5] Verifying Git installation...${NC}"
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git not installed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Git installed${NC}"
echo ""

# Step 2: Verify repository
echo -e "${BLUE}[2/5] Verifying local git repository...${NC}"
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Not in a git repository!${NC}"
    echo "Make sure you're in the loan_approval_system folder"
    exit 1
fi
echo -e "${GREEN}✓ Git repository found${NC}"
git log --oneline -1
echo ""

# Step 3: Check status
echo -e "${BLUE}[3/5] Checking git status...${NC}"
STATUS=$(git status --porcelain)
if [ ! -z "$STATUS" ]; then
    echo -e "${BLUE}ℹ️  Uncommitted changes:${NC}"
    echo "$STATUS"
    echo ""
    echo "Add and commit these changes first:"
    echo "  git add ."
    echo "  git commit -m 'Your message'"
    exit 1
fi
echo -e "${GREEN}✓ Working tree clean${NC}"
echo ""

# Step 4: Configure remote
echo -e "${BLUE}[4/5] Configuring GitHub remote...${NC}"
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "Adding remote: https://github.com/shilpakate/Gen_AI_Project_June_2026.git"
    git remote add origin https://github.com/shilpakate/Gen_AI_Project_June_2026.git
    echo -e "${GREEN}✓ Remote added${NC}"
else
    echo "Remote already configured:"
    git remote get-url origin
    echo -e "${GREEN}✓ Remote verified${NC}"
fi
echo ""

# Step 5: Ensure main branch
echo -e "${BLUE}[5/5] Switching to main branch...${NC}"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" != "main" ]; then
    echo "Switching to main branch..."
    git branch -M main
fi
echo -e "${GREEN}✓ On main branch${NC}"
echo ""

# Show what will be pushed
echo "📊 Ready to push:"
git log --oneline -5
echo ""
echo "Total files: $(git ls-files | wc -l)"
echo "Total commits: $(git rev-list --count HEAD)"
echo ""

# Final confirmation
echo "⚠️  IMPORTANT:"
echo "  You will be asked for GitHub credentials"
echo "  - Username: shilpakate"
echo "  - Password: Use Personal Access Token (NOT your password)"
echo "  - Get token: https://github.com/settings/tokens"
echo ""
read -p "Ready to push? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Push cancelled"
    exit 0
fi

echo ""
echo "🔄 Pushing to GitHub..."
echo ""

# Push
if git push -u origin main; then
    echo ""
    echo "================================================================================"
    echo -e "${GREEN}✅ SUCCESS! CODE PUSHED TO GITHUB${NC}"
    echo "================================================================================"
    echo ""
    echo "📍 Your repository:"
    echo "   https://github.com/shilpakate/Gen_AI_Project_June_2026"
    echo ""
    echo "📊 Summary:"
    git log --oneline -1
    echo ""
    echo "📦 Files pushed: $(git ls-files | wc -l)"
    echo ""
    echo "✅ Next steps:"
    echo "   1. Go to: https://github.com/shilpakate/Gen_AI_Project_June_2026"
    echo "   2. Verify all files are visible"
    echo "   3. Share the repository URL with others"
    echo "   4. Clone to test: git clone https://github.com/shilpakate/Gen_AI_Project_June_2026.git"
    echo ""
    echo "================================================================================"
else
    echo ""
    echo "================================================================================"
    echo -e "${RED}❌ PUSH FAILED${NC}"
    echo "================================================================================"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check internet connection: ping github.com"
    echo "  2. Verify GitHub username: shilpakate"
    echo "  3. Use Personal Access Token for password"
    echo "  4. Get token: https://github.com/settings/tokens"
    echo ""
    exit 1
fi

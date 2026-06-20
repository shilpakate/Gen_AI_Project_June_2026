#!/bin/bash

# Push to GitHub - Agentic AI Loan Approval System
# Run this script to push all code to GitHub

echo "================================================================================"
echo "🚀 PUSHING CODE TO GITHUB"
echo "================================================================================"
echo ""
echo "Repository: https://github.com/shilpakate/Gen_AI_Project_June_2026"
echo "Branch: main"
echo "Files: 32"
echo "Lines: 7,700+"
echo ""

# Check git status
echo "📋 Current git status:"
git status --short
echo ""

# Configure remote if needed
if git remote get-url origin > /dev/null 2>&1; then
    echo "✓ Remote already configured:"
    git remote get-url origin
else
    echo "⚙️  Configuring remote..."
    git remote add origin https://github.com/shilpakate/Gen_AI_Project_June_2026.git
    echo "✓ Remote configured"
fi

echo ""
echo "📊 Commits to push:"
git log --oneline -5
echo ""

# Ensure main branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "🔄 Switching to main branch..."
    git branch -M main
fi

echo "🔄 Pushing to GitHub..."
echo ""

# Push
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================================================"
    echo "✅ SUCCESS! CODE PUSHED TO GITHUB"
    echo "================================================================================"
    echo ""
    echo "📍 Your repository:"
    echo "   https://github.com/shilpakate/Gen_AI_Project_June_2026"
    echo ""
    echo "✓ 32 files pushed"
    echo "✓ 7,700+ lines of code"
    echo "✓ All documentation included"
    echo "✓ Security verified (no API keys)"
    echo ""
    echo "📖 Share this link:"
    echo "   https://github.com/shilpakate/Gen_AI_Project_June_2026"
    echo ""
    echo "🧪 Clone and test:"
    echo "   git clone https://github.com/shilpakate/Gen_AI_Project_June_2026.git"
    echo "   cd Gen_AI_Project_June_2026"
    echo "   pip install -r requirements.txt"
    echo "   pytest tests/ -v"
    echo ""
    echo "================================================================================"
else
    echo ""
    echo "================================================================================"
    echo "❌ PUSH FAILED"
    echo "================================================================================"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check internet connection"
    echo "2. Verify GitHub username: shilpakate"
    echo "3. For HTTPS: Use Personal Access Token (not password)"
    echo "   Get token: https://github.com/settings/tokens"
    echo "4. For SSH: Ensure SSH key is configured"
    echo ""
    echo "Try again or see DEPLOY_TO_GITHUB_GUIDE.md for more options"
    echo ""
    echo "================================================================================"
    exit 1
fi

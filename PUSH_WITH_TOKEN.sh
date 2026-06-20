#!/bin/bash

# GitHub Push Script with Personal Access Token
# Usage: ./PUSH_WITH_TOKEN.sh <your_personal_access_token>

if [ -z "$1" ]; then
    echo "=================================================================================="
    echo "❌ ERROR: Personal Access Token required"
    echo "=================================================================================="
    echo ""
    echo "Usage: ./PUSH_WITH_TOKEN.sh YOUR_GITHUB_TOKEN"
    echo ""
    echo "To get your token:"
    echo "  1. Go to: https://github.com/settings/tokens"
    echo "  2. Click 'Generate new token' → 'Generate new token (classic)'"
    echo "  3. Name: 'loan_approval_system'"
    echo "  4. Select scopes: repo, write:packages"
    echo "  5. Copy the token (starts with ghp_)"
    echo ""
    echo "Then run:"
    echo "  ./PUSH_WITH_TOKEN.sh ghp_YOUR_TOKEN_HERE"
    echo ""
    echo "=================================================================================="
    exit 1
fi

TOKEN=$1
REPO_URL="https://shilpakate:${TOKEN}@github.com/shilpakate/Gen_AI_Project_June_2026.git"

echo "=================================================================================="
echo "🚀 PUSHING CODE TO GITHUB WITH TOKEN"
echo "=================================================================================="
echo ""
echo "Repository: https://github.com/shilpakate/Gen_AI_Project_June_2026"
echo "Branch: main"
echo "Files: $(git ls-files | wc -l)"
echo ""

# Remove old remote
echo "Updating remote URL..."
git remote remove origin 2>/dev/null
git remote add origin "$REPO_URL"

echo "Pushing to GitHub..."
echo ""

# Push
if git push -u origin main; then
    echo ""
    echo "=================================================================================="
    echo "✅ SUCCESS! CODE PUSHED TO GITHUB"
    echo "=================================================================================="
    echo ""
    echo "Repository: https://github.com/shilpakate/Gen_AI_Project_June_2026"
    echo ""
    echo "Pushed files:"
    git log --oneline -1
    echo ""
    echo "Total files: $(git ls-files | wc -l)"
    echo "Total commits: $(git rev-list --count HEAD)"
    echo ""
    echo "✅ Your code is now live on GitHub!"
    echo ""
    echo "Next steps:"
    echo "  1. Visit: https://github.com/shilpakate/Gen_AI_Project_June_2026"
    echo "  2. Verify all files are visible"
    echo "  3. Share the repository URL"
    echo ""
    echo "=================================================================================="
    exit 0
else
    echo ""
    echo "=================================================================================="
    echo "❌ PUSH FAILED"
    echo "=================================================================================="
    echo ""
    echo "Troubleshooting:"
    echo "  • Check token is correct"
    echo "  • Token might have expired"
    echo "  • Repository might not exist yet"
    echo "  • Check GitHub status: https://www.githubstatus.com"
    echo ""
    exit 1
fi

#!/usr/bin/env bash
# Automated RUSH Lab submission script
# This script prepares everything for submission

set -euo pipefail

echo "=============================================="
echo "🚀 RUSH Lab Plugin Submission Script"
echo "=============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

REPO_URL="https://github.com/raha2079/travel-planning"

echo -e "${BLUE}Plugin:${NC} Travel Planning"
echo -e "${BLUE}Repository:${NC} $REPO_URL"
echo -e "${BLUE}GitHub User:${NC} raha2079"
echo ""

# Step 1: Verify local setup
echo -e "${YELLOW}Step 1: Verifying local setup...${NC}"
./run.sh
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Local tests passed${NC}"
else
    echo -e "${RED}✗ Local tests failed - fix errors before submitting${NC}"
    exit 1
fi
echo ""

# Step 2: Verify GitHub repository
echo -e "${YELLOW}Step 2: Verifying GitHub repository...${NC}"
if git remote get-url origin &> /dev/null; then
    echo -e "${GREEN}✓ Git remote configured${NC}"
    echo "  Remote: $(git remote get-url origin)"
else
    echo -e "${RED}✗ Git remote not configured${NC}"
    exit 1
fi

# Check if everything is pushed
if [ -z "$(git status --porcelain)" ]; then
    echo -e "${GREEN}✓ All changes committed${NC}"
else
    echo -e "${YELLOW}⚠ Uncommitted changes detected${NC}"
    git status --short
    read -p "Commit and push changes? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "Updates before RUSH Lab submission"
        git push
        echo -e "${GREEN}✓ Changes pushed to GitHub${NC}"
    fi
fi
echo ""

# Step 3: Check GitHub repository is accessible
echo -e "${YELLOW}Step 3: Checking GitHub repository accessibility...${NC}"
if curl -s -o /dev/null -w "%{http_code}" "$REPO_URL" | grep -q "200"; then
    echo -e "${GREEN}✓ Repository is public and accessible${NC}"
else
    echo -e "${RED}✗ Repository not accessible - ensure it's public${NC}"
    exit 1
fi
echo ""

# Step 4: Check for RUSH Lab CLI
echo -e "${YELLOW}Step 4: Checking for RUSH Lab CLI...${NC}"
if command -v rush-lab &> /dev/null; then
    echo -e "${GREEN}✓ RUSH Lab CLI is installed${NC}"
    echo "  Version: $(rush-lab --version 2>/dev/null || echo 'unknown')"
    RUSH_LAB_INSTALLED=true
elif command -v rushlab &> /dev/null; then
    echo -e "${GREEN}✓ RUSH Lab CLI is installed (as 'rushlab')${NC}"
    echo "  Version: $(rushlab --version 2>/dev/null || echo 'unknown')"
    RUSH_LAB_INSTALLED=true
else
    echo -e "${YELLOW}⚠ RUSH Lab CLI not installed${NC}"
    RUSH_LAB_INSTALLED=false
fi
echo ""

# Step 5: Instructions for submission
echo "=============================================="
echo -e "${GREEN}✅ Plugin is ready for submission!${NC}"
echo "=============================================="
echo ""

if [ "$RUSH_LAB_INSTALLED" = true ]; then
    echo -e "${BLUE}Option 1: Submit via CLI (Recommended)${NC}"
    echo ""
    echo "Run this command:"
    echo -e "${GREEN}rush-lab plugin submit $REPO_URL${NC}"
    echo ""
    echo "Or:"
    echo -e "${GREEN}rush-lab plugin publish $REPO_URL${NC}"
    echo ""
else
    echo -e "${YELLOW}RUSH Lab CLI not installed.${NC}"
    echo ""
    echo "To install:"
    echo "1. Go to ${BLUE}https://rush-lab.org${NC}"
    echo "2. Sign in with GitHub (username: ${GREEN}raha2079${NC})"
    echo "3. Copy the installation command from the pop-up"
    echo "4. Run it in your terminal"
    echo ""
fi

echo -e "${BLUE}Option 2: Submit via Web Interface${NC}"
echo ""
echo "1. Go to ${BLUE}https://rush-lab.org${NC}"
echo "2. Sign in with GitHub"
echo "3. Navigate to Marketplace"
echo "4. Click 'Submit Plugin' or 'Add Plugin'"
echo "5. Enter this URL: ${GREEN}$REPO_URL${NC}"
echo "6. Click Submit"
echo ""

echo "=============================================="
echo -e "${BLUE}Quick Copy (for web submission):${NC}"
echo -e "${GREEN}$REPO_URL${NC}"
echo "=============================================="
echo ""

# Open RUSH Lab in browser if possible
if command -v open &> /dev/null; then
    read -p "Open RUSH Lab in browser now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open "https://rush-lab.org"
        echo -e "${GREEN}✓ Opened RUSH Lab in browser${NC}"
        echo "  Repository URL copied to clipboard (if available)"
        echo "$REPO_URL" | pbcopy 2>/dev/null || echo "$REPO_URL" | xclip -selection clipboard 2>/dev/null || true
    fi
elif command -v xdg-open &> /dev/null; then
    read -p "Open RUSH Lab in browser now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        xdg-open "https://rush-lab.org"
        echo -e "${GREEN}✓ Opened RUSH Lab in browser${NC}"
    fi
fi

echo ""
echo -e "${GREEN}Next steps:${NC}"
echo "1. Sign in to RUSH Lab with GitHub"
echo "2. Submit your plugin using the URL above"
echo "3. Wait for marketplace checks to complete"
echo "4. Take screenshots for your report"
echo ""
echo -e "${BLUE}Need help? Check PUBLISH_NOW.md${NC}"

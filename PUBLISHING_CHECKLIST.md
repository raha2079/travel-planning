# RUSH Lab Publishing Checklist

## ✅ Pre-Publishing Checklist (COMPLETED)

- [x] Plugin code complete
- [x] All tests passing
- [x] Git repository initialized
- [x] Code committed to git
- [x] GitHub repository created: https://github.com/raha2079/travel-planning
- [x] Code pushed to GitHub
- [x] README.md documentation complete
- [x] Verifier working correctly

## 📋 Publishing Steps (DO NOW)

### Step 1: Register Your Task (Deadline: October 22, 2026) ⚠️

**Action Required:** Add your information to the Google Sheet

1. Open the Google Sheet link provided by your course staff
2. Add a new row with:
   - **GitHub Username**: `raha2079`
   - **Task Name**: `Travel Planning`
   - **Brief Description**: `Budget-constrained flight and hotel selection with workflow verification`
   - **Repository URL**: `https://github.com/raha2079/travel-planning`

**Why**: TAs use this to invite you to RUSH Lab.

---

### Step 2: Access RUSH Lab Website

**Action Required:** Sign in to RUSH Lab

1. Open your browser and go to: **https://rush-lab.org**
2. Click the **"Sign in with GitHub"** button
3. Authorize RUSH Lab to access your GitHub account `raha2079`
4. You should see a pop-up with installation instructions

---

### Step 3: Install RUSH Lab CLI

**Action Required:** Install the RUSH Lab command-line tool

1. A pop-up should appear on the RUSH Lab website showing an installation command
2. Copy the command (it will look something like this):
   ```bash
   curl -fsSL https://rush-lab.org/install.sh | sh
   ```
   or
   ```bash
   npm install -g @rush-lab/cli
   ```
   (The exact command will be shown in the pop-up)

3. Open your terminal and run the command
4. Follow any additional prompts

**If you have trouble:**
- Contact the TAs immediately (before deadline)
- Check that you're on macOS/Linux (use WSL on Windows)

---

### Step 4: Get OpenRouter API Key

**Action Required:** Create and configure API key

1. Go to: **https://openrouter.ai/**
2. Sign up or sign in
3. Go to **API Keys** section
4. Create a new API key
5. Copy the API key (save it securely - you won't see it again!)
6. In RUSH Lab:
   - Go to **Settings → Usage**
   - Paste your OpenRouter API key
   - Save

**Note**: You can use the TAs' provided key ($10/month cap) or your own key.

---

### Step 5: Submit Plugin to Marketplace

**Action Required:** Publish your plugin

#### Option A: Via RUSH Lab Web Interface (Recommended)

1. In RUSH Lab, navigate to **Marketplace**
2. Click **"Submit Plugin"** or **"Add Plugin"**
3. Enter your GitHub repository URL:
   ```
   https://github.com/raha2079/travel-planning
   ```
4. Click **Submit**
5. Wait for marketplace checks to complete

#### Option B: Via CLI (If available)

```bash
rush-lab plugin publish https://github.com/raha2079/travel-planning
```

---

### Step 6: Fix Any Errors

**Action Required:** Review and fix marketplace checks

If the marketplace reports errors:

1. **Review the error messages** - they tell you exactly what's wrong
2. **Common issues:**
   - Missing files → Check all required files exist
   - Invalid YAML → Validate `nanoagent.yaml` syntax
   - Python errors → Check `contract.py` imports
   - File structure → Ensure `src/plugin/` exists

3. **Fix locally:**
   ```bash
   cd /Users/gray/Documents/everyday_agent_evals_v3/travel-planning
   # Make your fixes
   git add .
   git commit -m "Fix marketplace errors"
   git push
   ```

4. **Resubmit** the plugin after pushing fixes

---

### Step 7: Verify Publication

**Action Required:** Confirm plugin is live

1. Check that your plugin appears in the RUSH Lab marketplace
2. Look for: **"Travel Planning"** by `raha2079`
3. Verify the plugin shows:
   - ✓ Name: Travel Planning
   - ✓ Description visible
   - ✓ Status: Ready
   - ✓ Tools: 5 tools listed

---

### Step 8: Test Your Plugin (Optional but Recommended)

**Action Required:** Run a test to verify everything works

1. In RUSH Lab, create a **New Task Run**
2. Select your plugin: **Travel Planning**
3. Use test data from your repository:
   - Copy contents from `tests/request.json`
   - Copy contents from `tests/options.json`
4. **Run the agent**
5. **Check results:**
   - Agent should call all 5 tools in order
   - Verifier should return PASS
   - Budget should be within limit ($1560 ≤ $1800)

---

## 🎯 Quick Reference

**Repository URL**: https://github.com/raha2079/travel-planning

**GitHub Username**: raha2079

**Plugin ID**: travel-planning

**RUSH Lab URL**: https://rush-lab.org

**OpenRouter**: https://openrouter.ai/

---

## ⚠️ Important Deadlines

- **October 22, 2026**: Register on Google Sheet (REQUIRED)
- **November 2, 2026**: Project milestone due

---

## 📞 Getting Help

- **RUSH Lab Installation Issues**: Contact TAs immediately
- **GitHub Issues**: https://github.com/RUSH-LAB/nanoagent/issues
- **Plugin Errors**: Check `SETUP_GUIDE.md` troubleshooting section

---

## ✅ After Publishing

Once your plugin is published and working:

1. [ ] Take screenshots of:
   - Plugin in marketplace
   - Successful test run
   - Verifier output showing PASS
2. [ ] Document any issues encountered
3. [ ] Prepare for your project report:
   - Why is the task objectively verifiable?
   - How is the environment reproducible?
   - How does the verifier handle incorrect outputs?
   - What limitations remain?

---

## Status Tracker

- [ ] Registered on Google Sheet
- [ ] Signed in to RUSH Lab
- [ ] RUSH Lab CLI installed
- [ ] OpenRouter API key configured
- [ ] Plugin submitted to marketplace
- [ ] Marketplace checks passed
- [ ] Plugin visible in marketplace
- [ ] Test run completed successfully

**Last Updated**: October 16, 2026

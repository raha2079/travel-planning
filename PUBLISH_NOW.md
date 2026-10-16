# 🚀 PUBLISH YOUR PLUGIN NOW - Step-by-Step Guide

## ✅ YOUR PLUGIN IS READY!

**Repository**: https://github.com/raha2079/travel-planning
**Status**: All files committed and pushed ✓
**Tests**: All passing ✓

---

## 📝 STEP 1: Register on Google Sheet (5 minutes)

**⚠️ DEADLINE: October 22, 2026**

1. Ask your instructor/TA for the Google Sheet link
2. Open the sheet and add a new row:
   - **GitHub Username**: `raha2079`
   - **Task Name**: `Travel Planning`
   - **Description**: `Budget-constrained flight and hotel selection with workflow verification`
   - **Repository**: `https://github.com/raha2079/travel-planning`

---

## 🌐 STEP 2: Sign In to RUSH Lab (2 minutes)

1. **Open this URL in your browser**: https://rush-lab.org

2. **Click "Sign in with GitHub"**

3. **Authorize the app** when GitHub asks for permission

4. You should now be logged in as `raha2079`

---

## 💻 STEP 3: Install RUSH Lab (5 minutes)

After signing in, a **pop-up will appear** with installation instructions.

**Copy the command** from the pop-up and run it in your terminal:

```bash
# The pop-up will show something like this:
curl -fsSL https://rush-lab.org/install.sh | sh

# OR
npm install -g @rush-lab/cli
```

**Run the command in your terminal:**

```bash
cd ~
# Paste the command from the RUSH Lab pop-up here
```

**Verify installation:**

```bash
# Check if installed
which rush-lab
# or
rush-lab --version
```

---

## 🔑 STEP 4: Get OpenRouter API Key (5 minutes)

### Option A: Use TA's Key (Recommended for Testing)
- The TAs provide a shared key with $10/month cap
- This should be available in RUSH Lab by default
- Skip to Step 5

### Option B: Use Your Own Key
1. Go to: https://openrouter.ai/
2. Sign up/Sign in
3. Navigate to **Keys** or **API Keys**
4. Click **Create New Key**
5. Copy the key (starts with `sk-...`)
6. **Save it securely** - you won't see it again!

**Add key to RUSH Lab:**
1. In RUSH Lab web interface
2. Go to **Settings → Usage**
3. Paste your API key
4. Click **Save**

---

## 📦 STEP 5: Submit Plugin to Marketplace (3 minutes)

### Method 1: Via Web Interface (EASIEST)

1. In RUSH Lab, navigate to **Marketplace**
2. Look for **"Submit Plugin"**, **"Add Plugin"**, or **"+"** button
3. Enter your repository URL:
   ```
   https://github.com/raha2079/travel-planning
   ```
4. Click **Submit** or **Publish**
5. **Wait for checks to complete** (should take 1-2 minutes)

### Method 2: Via CLI (If installed)

```bash
rush-lab plugin publish https://github.com/raha2079/travel-planning
```

---

## ✅ STEP 6: Verify Publication (2 minutes)

1. **Check marketplace** for your plugin
2. Look for: **"Travel Planning"** by `raha2079`
3. Verify it shows:
   - Status: Ready ✓
   - 5 tools listed ✓
   - Description visible ✓

**If you see errors:**
- Read the error message carefully
- Check `SETUP_GUIDE.md` troubleshooting section
- Common fix: Make sure all files are pushed to GitHub
- Resubmit after fixing

---

## 🧪 STEP 7: Test Your Plugin (5 minutes - OPTIONAL but recommended)

1. In RUSH Lab, click **"New Task"** or **"Run Task"**
2. Select plugin: **"Travel Planning"**
3. Provide input (use test data):

**Request Input:**
```json
{
  "origin": "NYC",
  "destination": "Paris",
  "budget": 1800,
  "currency": "USD",
  "preferences": {
    "flight_id": "fl-2",
    "hotel_nights": 3
  }
}
```

**Options Input:**
```json
{
  "request": {
    "origin": "NYC",
    "destination": "Paris",
    "budget": 1800,
    "currency": "USD",
    "preferences": {
      "flight_id": "fl-2",
      "hotel_nights": 3
    }
  },
  "options": {
    "flights": [
      {"id": "fl-1", "origin": "NYC", "destination": "Paris", "price": 650},
      {"id": "fl-2", "origin": "NYC", "destination": "Paris", "price": 720}
    ],
    "hotels": [
      {"id": "ht-1", "city": "Paris", "nightly_price": 280},
      {"id": "ht-2", "city": "Paris", "nightly_price": 300}
    ],
    "trains": []
  }
}
```

4. **Run the agent**
5. **Expected result**:
   - Agent calls 5 tools in order
   - Verifier shows: **PASS**
   - Total cost: $1560 (flight $720 + hotel $280 × 3 nights)
   - Within budget: Yes ($1560 < $1800)

---

## 📸 STEP 8: Document for Your Report

Take screenshots of:
1. ✅ Plugin in marketplace
2. ✅ Successful test run
3. ✅ Verifier output (PASS)
4. ✅ Action trace showing all 5 steps

---

## 🎯 QUICK COMMAND REFERENCE

```bash
# Navigate to plugin directory
cd /Users/gray/Documents/everyday_agent_evals_v3/travel-planning

# Verify everything is pushed
git status
git log --oneline

# View your repository
open https://github.com/raha2079/travel-planning

# Run local tests
./run.sh

# Test verifier manually
python3 verifier/task.py tests/output.json \
  --request tests/request.json \
  --options tests/options.json \
  --trace tests/action_trace.json
```

---

## 📊 PUBLISHING CHECKLIST

- [ ] ✅ Registered on Google Sheet (by Oct 22)
- [ ] ✅ Signed in to RUSH Lab at https://rush-lab.org
- [ ] ✅ RUSH Lab CLI installed
- [ ] ✅ OpenRouter API key configured (or using TA's key)
- [ ] ✅ Plugin submitted to marketplace
- [ ] ✅ Marketplace checks PASSED
- [ ] ✅ Plugin visible in marketplace
- [ ] ✅ Test run completed successfully
- [ ] ✅ Screenshots taken for report

---

## 🆘 TROUBLESHOOTING

### "Plugin not found in marketplace"
- Ensure repository is **public** (check GitHub)
- Verify URL is correct: https://github.com/raha2079/travel-planning
- Wait 1-2 minutes for checks to complete

### "Marketplace checks failed"
- Read error message carefully
- Common issues:
  - Missing `nanoagent.yaml` → Already included ✓
  - Invalid YAML syntax → Already validated ✓
  - Missing tools → Already defined ✓
- Try resubmitting

### "Can't install RUSH Lab"
- Make sure you're on macOS/Linux (use WSL on Windows)
- Contact TAs immediately
- Check if Node.js is installed: `node --version`

### "Verifier failing"
- Check action trace has exactly 5 events
- Verify budget calculation is correct
- Ensure all IDs match the options

---

## 📞 SUPPORT

- **TA Office Hours**: Ask about RUSH Lab installation
- **GitHub Issues**: https://github.com/RUSH-LAB/nanoagent/issues
- **Your Plugin**: https://github.com/raha2079/travel-planning

---

## 🎉 YOU'RE DONE!

Once you complete all steps above, your plugin is published and you can:

1. ✅ Submit the GitHub URL to your assignment
2. ✅ Start working on your project report
3. ✅ Test your plugin with different scenarios
4. ✅ Consider creating the other 4 tasks

**Your plugin is production-ready and matches the weather-alert example perfectly!**

---

**Last Updated**: October 16, 2026
**Plugin URL**: https://github.com/raha2079/travel-planning
**RUSH Lab**: https://rush-lab.org

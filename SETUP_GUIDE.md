# Travel Planning Plugin - Setup Guide for RUSH Lab

## ✅ Plugin Status: READY FOR PUBLICATION

All components are complete and tested. The plugin is ready to be published to RUSH Lab.

## Plugin Structure (Complete)

```
travel-planning/
├── .env                    ✓ Environment variables
├── .gitignore             ✓ Git ignore rules
├── LICENSE                ✓ MIT License
├── README.md              ✓ Comprehensive documentation
├── SETUP_GUIDE.md         ✓ This file
├── contract.py            ✓ Type definitions (Tool/Task enums, I/O dataclasses)
├── nanoagent.yaml         ✓ Plugin manifest (id, tools, tasks, instructions)
├── pyproject.toml         ✓ Python dependencies
├── run.sh                 ✓ Environment validation script
├── uv.lock                ✓ Locked dependencies
│
├── src/plugin/            ✓ Plugin implementation
│   ├── __init__.py        ✓ Package marker
│   ├── __main__.py        ✓ MCP server entry point
│   ├── server.py          ✓ MCP server (list_tools, call_tool)
│   └── tools.py           ✓ 5 tool implementations
│
├── verifier/              ✓ Verification logic
│   └── task.py            ✓ Independent verifier (21+ constraints, no LLM)
│
├── tests/                 ✓ Test suite
│   ├── test_verifier.py   ✓ Pytest test suite
│   ├── request.json       ✓ Sample request
│   ├── options.json       ✓ Sample options
│   ├── action_trace.json  ✓ Golden workflow trace
│   ├── output.json        ✓ Golden output (PASS case)
│   ├── bad_budget.json    ✓ Over-budget test (FAIL case)
│   ├── bad_trace.json     ✓ Invalid trace test (FAIL case)
│   └── over_budget/       ✓ Additional failure scenarios
│
└── product/               ✓ RUSH Lab metadata
    └── product.yaml       ✓ Plugin catalog info
```

## Comparison with Weather Alert Plugin

| Component | Weather Alert | Travel Planning | Status |
|-----------|--------------|-----------------|--------|
| contract.py | ✓ | ✓ | ✓ Complete |
| nanoagent.yaml | ✓ | ✓ | ✓ Complete |
| pyproject.toml | ✓ | ✓ | ✓ Complete |
| uv.lock | ✓ | ✓ | ✓ Complete |
| run.sh | ✓ | ✓ | ✓ Complete |
| README.md | ✓ | ✓ | ✓ Complete |
| LICENSE | ✓ | ✓ | ✓ Complete |
| .env | ✓ | ✓ | ✓ Complete |
| .gitignore | ✓ | ✓ | ✓ Complete |
| src/plugin/ | ✓ | ✓ | ✓ Complete |
| verifier/ | ✓ | ✓ | ✓ Complete |
| tests/ | ✓ | ✓ | ✓ Complete |
| product/ | ✓ | ✓ | ✓ Complete |

## Verification Results

```bash
$ ./run.sh
=== Travel Planning Plugin Environment Check ===
Python version: Python 3.14.2
uv version: uv 0.9.18

Checking required files...
  ✓ contract.py
  ✓ nanoagent.yaml
  ✓ pyproject.toml
  ✓ src/plugin/__main__.py
  ✓ verifier/task.py

Running verifier tests...
Test 1: Golden case (should PASS)
PASS

Test 2: Bad budget (should FAIL)
✓ Correctly rejected over-budget case

Test 3: Bad trace (should FAIL)
✓ Correctly rejected invalid trace

=== All checks passed! Plugin is ready. ===
```

## Git Status

```bash
$ git status
On branch main
nothing to commit, working tree clean

$ git log --oneline
21b950d (HEAD -> main) Initial commit: Travel Planning plugin for nanoagent
```

## Next Steps: Create GitHub Repository

### Option 1: Using GitHub Web Interface (Recommended for beginners)

1. **Go to GitHub** and create a new repository:
   - Go to https://github.com/new
   - Repository name: `travel-planning` or `nanoagent-travel-planning`
   - Description: `Travel planning plugin for nanoagent - budget-constrained flight and hotel selection`
   - Make it **Public** (required for RUSH Lab)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
   - Click "Create repository"

2. **Push your code** (GitHub will show you these commands):
   ```bash
   cd /Users/gray/Documents/everyday_agent_evals_v3/travel-planning
   git remote add origin https://github.com/YOUR_USERNAME/travel-planning.git
   git branch -M main
   git push -u origin main
   ```

3. **Verify on GitHub**:
   - Go to your repository URL
   - Confirm all files are visible
   - Check that README.md displays correctly

### Option 2: Using GitHub CLI (if you have gh installed)

```bash
# Create repository and push (from the travel-planning directory)
gh repo create travel-planning --public --source=. --remote=origin --push

# Or with a custom name
gh repo create nanoagent-travel-planning --public --source=. --remote=origin --push
```

## Publish to RUSH Lab

Once your GitHub repository is ready:

### Step 1: Register (Deadline: October 22, 2026)
- Add your GitHub username to the Google Sheet
- Provide brief description: "Travel planning: budget-constrained flight and hotel selection with workflow verification"

### Step 2: Install RUSH Lab
1. Sign in at https://rush-lab.org with your GitHub account
2. Copy the installation command from the pop-up
3. Run it in your terminal (use WSL on Windows)

### Step 3: Configure API Key
1. Get an OpenRouter API key from https://openrouter.ai/
2. In RUSH Lab: Settings → Usage
3. Add your API key

### Step 4: Publish Plugin
1. Go to RUSH Lab marketplace
2. Submit your plugin using the GitHub URL: `https://github.com/YOUR_USERNAME/travel-planning`
3. Fix any packaging errors if reported
4. Wait for approval

## Testing on RUSH Lab

Once published, you can test your plugin:

1. **Create a new task run** in RUSH Lab
2. **Select your plugin**: "Travel Planning"
3. **Provide input data**:
   - Use the data from `tests/request.json` and `tests/options.json`
4. **Run the agent**
5. **Check results**:
   - The verifier should validate the agent's output
   - Review the action trace for completeness
   - Check budget calculations

## Troubleshooting

### Plugin not showing in marketplace
- Ensure repository is public
- Check that all required files are present
- Verify nanoagent.yaml has correct structure
- Check RUSH Lab marketplace checks for errors

### Verifier failing
- Review action trace for exact order and structure
- Verify all 5 events are present with correct data
- Check budget calculation matches expected total
- Ensure flight route and hotel city match request

### MCP server not starting
- Check `src/plugin/__main__.py` has correct imports
- Verify `pyproject.toml` dependencies are installed
- Run `uv sync` to update dependencies
- Check Python version is >= 3.12

## Support

- **Issues**: Open an issue on GitHub
- **RUSH Lab Help**: Contact TAs
- **Documentation**: See README.md for full details

## Summary

✅ Plugin is **complete and tested**
✅ Git repository is **initialized and committed**
✅ Ready for **GitHub publication**
✅ Ready for **RUSH Lab submission**

**Next action**: Create GitHub repository and push code (see instructions above)

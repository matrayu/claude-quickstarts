

# Autonomous Coding Agent - Standalone Tool Guide

## Understanding the Architecture

This tool separates **core functionality** from **project-specific configuration**:

```
~/.autonomous-coding-agent/           # ← ONE installation (core tool)
├── autonomous_agent_demo.py          # ← Fix bugs HERE
├── agent.py                          # ← Updates propagate everywhere
├── client.py
├── security.py
├── progress.py
├── prompts.py
├── requirements.txt
├── venv/                             # Shared virtual environment
└── prompts/
    ├── initializer_prompt.md
    ├── coding_prompt.md
    └── app_spec.txt                  # Example only

~/my-projects/todo-app/               # ← PROJECT A
├── .autonomous-coding/
│   ├── config.json                   # Feature count: 50, model: sonnet
│   └── app_spec.txt                  # Todo app specification
└── generations/
    └── todo-app/                     # Generated application

~/my-projects/blog-platform/         # ← PROJECT B
├── .autonomous-coding/
│   ├── config.json                   # Feature count: 100, model: opus
│   └── app_spec.txt                  # Blog platform specification
└── generations/
    └── blog-platform/                # Generated application
```

## Installation (Once)

```bash
cd /Users/206853553/Projects/personal/claude-quickstarts/autonomous-coding
./install-global.sh
```

**What this does:**
1. Copies core files to `~/.autonomous-coding-agent/`
2. Creates Python venv with dependencies
3. Installs `autonomous-coding` command in `~/.local/bin/`
4. Sets everything up for updates

**One-time PATH setup:**
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## Creating a New Project

### 1. Navigate to your project directory
```bash
mkdir ~/my-projects/my-saas-app
cd ~/my-projects/my-saas-app
```

### 2. Initialize
```bash
autonomous-coding init
```

**You'll be prompted for:**
- **App Specification**: Create new, use example, or provide path
- **Feature Count**: How many test cases (20-200)
- **Model**: Sonnet 4.5, Opus 4.5, or Haiku 4.5
- **API Key**: Use environment variable or save in config

**What gets created:**
```
~/my-projects/my-saas-app/
└── .autonomous-coding/
    ├── config.json         # Your settings
    └── app_spec.txt        # Your app description
```

### 3. Review/Edit App Spec
```bash
vim .autonomous-coding/app_spec.txt
```

### 4. Start the Agent
```bash
autonomous-coding start
```

**What happens:**
- Creates `generations/my-saas-app/` directory
- Copies app_spec.txt to project
- Runs initializer agent (generates feature list)
- Begins implementing features
- Auto-continues every 3 seconds

### 5. Pause/Resume
```bash
# Pause
Ctrl+C

# Resume later
cd ~/my-projects/my-saas-app
autonomous-coding start
```

## Working with Multiple Projects

Each project is independent:

```bash
# Project 1: Todo App (quick demo)
cd ~/projects/todo-app
autonomous-coding init          # 20 features, Sonnet
autonomous-coding start --max-iterations 3

# Project 2: Blog Platform (full build)
cd ~/projects/blog-platform
autonomous-coding init          # 150 features, Opus
autonomous-coding start

# Project 3: Dashboard
cd ~/projects/analytics-dashboard
autonomous-coding init          # 80 features, Sonnet
autonomous-coding start
```

## Updating the Tool (Propagates to All Projects!)

When you find a bug in the core tool:

### Fix Once
```bash
cd ~/.autonomous-coding-agent

# Edit the buggy file
vim client.py  # Fix the issue

# OR pull latest fixes from quickstarts
autonomous-coding update
```

### Applies Everywhere
```bash
# All projects automatically use the fixed code!
cd ~/projects/todo-app
autonomous-coding start         # ← Uses fixed client.py

cd ~/projects/blog-platform
autonomous-coding start         # ← Uses fixed client.py

cd ~/projects/dashboard
autonomous-coding start         # ← Uses fixed client.py
```

## Contributing Fixes Back

Found and fixed a bug? Share it back:

```bash
# Copy your fix back to quickstarts
cd /Users/206853553/Projects/personal/claude-quickstarts/autonomous-coding
cp ~/.autonomous-coding-agent/client.py ./

# Commit
git add client.py
git commit -m "fix: better Playwright selector handling"

# Now others can benefit
git push
```

## File Organization

### Core Tool Files (in ~/.autonomous-coding-agent/)
- `autonomous_agent_demo.py` - Main entry point
- `agent.py` - Session management
- `client.py` - Claude SDK configuration
- `security.py` - Bash command security
- `progress.py` - Progress tracking
- `prompts.py` - Prompt utilities
- `requirements.txt` - Python dependencies

**These are SHARED across all projects** - fix bugs once!

### Project-Specific Files (in each project)
- `.autonomous-coding/config.json` - Project settings
- `.autonomous-coding/app_spec.txt` - App description
- `generations/` - Generated code

**These are UNIQUE per project** - customize freely!

## Examples

### Example 1: Quick Todo App Demo
```bash
cd ~/Desktop
mkdir quick-todo-demo && cd quick-todo-demo

autonomous-coding init
# Choose: 1 (create new)
# App name: Simple Todo List
# Description: Basic todo app with add/delete/complete
# Frontend: React
# Backend: Node.js
# Database: SQLite
# Features: 20
# Model: Sonnet

autonomous-coding start --max-iterations 3
```

### Example 2: Full E-commerce Platform
```bash
cd ~/projects
mkdir shopify-clone && cd shopify-clone

autonomous-coding init
# Choose: 1 (create new)
# [Fill in comprehensive e-commerce details]
# Features: 200
# Model: Opus

autonomous-coding start
# Let it run for hours/days
```

### Example 3: Using Existing Spec
```bash
cd ~/projects
mkdir api-gateway && cd api-gateway

# Create detailed spec first
vim my-api-spec.txt

autonomous-coding init
# Choose: 3 (provide path)
# Path: ./my-api-spec.txt
# Features: 100
# Model: Sonnet

autonomous-coding start
```

## Advanced Usage

### Custom Model
Edit `.autonomous-coding/config.json`:
```json
{
  "feature_count": 50,
  "model": "claude-opus-4-5-20251101",
  "api_key_source": "environment"
}
```

### Change Feature Count Mid-Project
```bash
# Edit config
vim .autonomous-coding/config.json
# Change "feature_count": 50 → 100

# Delete existing feature list to regenerate
rm generations/*/feature_list.json

# Restart
autonomous-coding start
```

### Use Different API Key Per Project
```bash
autonomous-coding init
# Choose to save API key in config

# Edit to change
vim .autonomous-coding/config.json
```

## Troubleshooting

### "Command not found: autonomous-coding"
```bash
# Check installation
ls ~/.autonomous-coding-agent
ls ~/.local/bin/autonomous-coding

# Check PATH
echo $PATH | grep -o "$HOME/.local/bin"

# Add to PATH if missing
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### "Not initialized in this directory"
```bash
# You need to run init first
autonomous-coding init
```

### "API key not set"
```bash
# Option 1: Environment variable (recommended)
export ANTHROPIC_API_KEY='your-key-here'
echo 'export ANTHROPIC_API_KEY="your-key"' >> ~/.zshrc

# Option 2: Save in project config
autonomous-coding init  # Choose to save key
```

### Update Not Working
```bash
# Manual update
cd ~/.autonomous-coding-agent

# Copy latest files from quickstarts
cp /Users/206853553/Projects/personal/claude-quickstarts/autonomous-coding/*.py ./
cp -r /Users/206853553/Projects/personal/claude-quickstarts/autonomous-coding/prompts ./

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt
```

### Want to Reinstall
```bash
# Remove old installation
rm -rf ~/.autonomous-coding-agent
rm ~/.local/bin/autonomous-coding

# Reinstall
cd /Users/206853553/Projects/personal/claude-quickstarts/autonomous-coding
./install-global.sh
```

## Best Practices

1. **One init per project** - Don't share .autonomous-coding/ between projects
2. **Version control app_spec** - Commit .autonomous-coding/app_spec.txt to your project repo
3. **Ignore generations/** - Add to .gitignore (agent creates git repos in there)
4. **Start small** - Test with 20-50 features before committing to 200
5. **Use max-iterations** - Test configurations with --max-iterations 3
6. **Update regularly** - Run `autonomous-coding update` to get bug fixes
7. **Document your spec** - Detailed app_spec.txt = better results

## Comparison: Before vs After

### Before (Quickstart Dependent)
❌ Had to run from quickstart directory
❌ All projects used same app_spec.txt
❌ Fixing bugs required updating each copy
❌ No easy way to customize per project
❌ Manual setup for each new project

### After (Standalone Tool)
✅ Run from any directory
✅ Each project has own app_spec.txt
✅ Fix bugs once, applies everywhere
✅ Easy per-project configuration
✅ Interactive init for new projects
✅ Clean separation of concerns

## Support

- **Tool location**: `~/.autonomous-coding-agent/`
- **Source**: `/Users/206853553/Projects/personal/claude-quickstarts/autonomous-coding/`
- **Command**: `autonomous-coding init|start|update`

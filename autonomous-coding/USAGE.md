# Using Autonomous Coding Agent Anywhere

## Quick Setup

### Option 1: Global Command (Recommended)

Install the agent as a global command you can run from anywhere:

```bash
cd /Users/206853553/Projects/personal/claude-quickstarts/autonomous-coding
./install.sh
```

Then use it from any directory:

```bash
# From any location
cd ~/my-projects
autonomous-coding-agent --project-dir ./my-app

# Or with absolute paths
autonomous-coding-agent --project-dir /path/to/my-project --max-iterations 10
```

### Option 2: Copy the Directory

Copy this autonomous-coding directory to wherever you want to use it:

```bash
# Copy to your projects folder
cp -r /Users/206853553/Projects/personal/claude-quickstarts/autonomous-coding ~/my-autonomous-agent

cd ~/my-autonomous-agent

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Use it
python autonomous_agent_demo.py --project-dir ./my-project
```

### Option 3: Fork & Maintain Your Own Version

```bash
# Create your own fork
cd ~/my-tools
git clone /Users/206853553/Projects/personal/claude-quickstarts claude-quickstarts-fork
cd claude-quickstarts-fork/autonomous-coding

# Set up
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Make your customizations, then commit
git add .
git commit -m "My custom configuration"
```

## Keeping Fixes in Sync

### If You Installed Globally (Option 1)

The global command always uses the original directory. When you make fixes:

```bash
cd /Users/206853553/Projects/personal/claude-quickstarts/autonomous-coding

# Make your changes to client.py, progress.py, etc.

# Commit them
git add .
git commit -m "fix: my improvement"

# No reinstall needed - changes take effect immediately!
```

### If You Copied (Option 2)

Pull fixes from the original:

```bash
# In your copied directory
cd ~/my-autonomous-agent

# Add the original as a remote
git remote add upstream /Users/206853553/Projects/personal/claude-quickstarts

# Pull latest fixes
git fetch upstream
git cherry-pick <commit-hash>  # Pick specific fixes
# OR
git merge upstream/main  # Merge all changes
```

### If You Forked (Option 3)

Same as Option 2 - use git to pull upstream changes.

## Customization Tips

### Change the App Being Built

Edit `prompts/app_spec.txt` with your desired application specification.

### Reduce Feature Count for Faster Demos

Edit `prompts/initializer_prompt.md`:
- Change "200 detailed" to "20 detailed" or any number you want

### Modify Security Settings

Edit `security.py` to add/remove allowed bash commands.

### Use Different Models

```bash
autonomous-coding-agent --project-dir ./my-app --model claude-opus-4-5-20251101
```

### Custom System Prompts

Edit `client.py` line 120 to customize the agent's behavior.

## Best Practices

1. **Always commit fixes** to your local branch
2. **Test with small feature counts first** (20-50 features)
3. **Use max-iterations for testing** new configurations
4. **Keep a backup** of your custom app_spec.txt files
5. **Document your changes** in commit messages

## Environment Variables

Required:
- `ANTHROPIC_API_KEY` - Your Anthropic API key

Optional:
- Can override in code if needed

## Generated Projects Location

By default, projects are created in `generations/` relative to where you run the command:

- If using global command: `./generations/[project-name]` in current directory
- Unless you specify absolute path: `--project-dir /absolute/path`

## Troubleshooting

### "ANTHROPIC_API_KEY not set"

```bash
export ANTHROPIC_API_KEY='your-key-here'
# Add to ~/.zshrc to persist
```

### "venv not found" (global command)

Re-run the install script or ensure venv exists in the autonomous-coding directory.

### "Permission denied" on tools

The fixes we made should prevent this. If you see it:
1. Check that your local copy has the latest client.py
2. Run `git pull` in the autonomous-coding directory

### Want to start fresh

```bash
# Remove generated project and start over
rm -rf generations/my-project
autonomous-coding-agent --project-dir ./my-project
```

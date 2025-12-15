#!/bin/bash
# Global Installation Script for Autonomous Coding Agent
# This installs the tool ONCE in ~/.autonomous-coding-agent

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOL_DIR="$HOME/.autonomous-coding-agent"
BIN_DIR="$HOME/.local/bin"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  AUTONOMOUS CODING AGENT - GLOBAL INSTALLATION                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# 1. Create tool directory
echo "📁 Creating tool directory..."
mkdir -p "$TOOL_DIR"
mkdir -p "$TOOL_DIR/prompts"
mkdir -p "$BIN_DIR"

# 2. Copy core files (project-agnostic)
echo "📦 Installing core tool files..."

core_files=(
    "autonomous_agent_demo.py"
    "agent.py"
    "client.py"
    "security.py"
    "progress.py"
    "prompts.py"
    "requirements.txt"
    "test_security.py"
)

for file in "${core_files[@]}"; do
    cp "$SCRIPT_DIR/$file" "$TOOL_DIR/"
    echo "  ✓ $file"
done

# 3. Copy prompt templates
echo "📄 Installing prompt templates..."
cp "$SCRIPT_DIR/prompts/"*.md "$TOOL_DIR/prompts/"
cp "$SCRIPT_DIR/prompts/app_spec.txt" "$TOOL_DIR/prompts/"
echo "  ✓ Prompts installed"

# 4. Copy CLI script
echo "🔧 Installing CLI..."
cp "$SCRIPT_DIR/autonomous-coding-cli.py" "$TOOL_DIR/"
chmod +x "$TOOL_DIR/autonomous-coding-cli.py"

# 5. Set up virtual environment
echo "🐍 Setting up Python virtual environment..."
cd "$TOOL_DIR"

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  ✓ Created virtual environment"
fi

source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "  ✓ Installed dependencies"

# 6. Create wrapper script in ~/.local/bin
echo "🔗 Creating command wrapper..."

cat > "$BIN_DIR/autonomous-coding" << 'WRAPPER_EOF'
#!/bin/bash
# Autonomous Coding Agent CLI Wrapper

TOOL_DIR="$HOME/.autonomous-coding-agent"

# Activate virtual environment and run CLI
source "$TOOL_DIR/venv/bin/activate"
python "$TOOL_DIR/autonomous-coding-cli.py" "$@"
WRAPPER_EOF

chmod +x "$BIN_DIR/autonomous-coding"
echo "  ✓ Created autonomous-coding command"

# 7. Check PATH
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  ✓ INSTALLATION COMPLETE                                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Tool installed to: $TOOL_DIR"
echo "Command available: $BIN_DIR/autonomous-coding"
echo ""

if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "⚠  Add $BIN_DIR to your PATH:"
    echo ""
    echo "   echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc"
    echo "   source ~/.zshrc"
    echo ""
else
    echo "✓ $BIN_DIR is already in your PATH"
    echo ""
fi

echo "Usage:"
echo "  cd ~/my-projects/new-app"
echo "  autonomous-coding init     # Interactive setup"
echo "  autonomous-coding start    # Run the agent"
echo ""
echo "Update the tool:"
echo "  autonomous-coding update   # Pull latest fixes"
echo ""
echo "Fix bugs in core files at:"
echo "  $TOOL_DIR/"
echo "  (Changes propagate to all projects automatically)"

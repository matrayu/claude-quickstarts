#!/bin/bash
# Installation script for autonomous coding agent

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.local/bin"

echo "Installing autonomous-coding-agent..."

# Create install directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Create wrapper script
cat > "$INSTALL_DIR/autonomous-coding-agent" << 'EOF'
#!/bin/bash
# Autonomous Coding Agent Wrapper

AGENT_DIR="__AGENT_DIR__"

cd "$AGENT_DIR"

# Activate virtual environment
source venv/bin/activate

# Run the agent with all arguments passed through
python autonomous_agent_demo.py "$@"
EOF

# Replace placeholder with actual directory
sed -i.bak "s|__AGENT_DIR__|$SCRIPT_DIR|g" "$INSTALL_DIR/autonomous-coding-agent"
rm "$INSTALL_DIR/autonomous-coding-agent.bak"

# Make executable
chmod +x "$INSTALL_DIR/autonomous-coding-agent"

echo "✓ Installed to $INSTALL_DIR/autonomous-coding-agent"
echo ""
echo "Add $INSTALL_DIR to your PATH if not already:"
echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc"
echo "  source ~/.zshrc"
echo ""
echo "Usage:"
echo "  autonomous-coding-agent --project-dir ./my-project"
echo "  autonomous-coding-agent --project-dir /absolute/path/to/project --max-iterations 5"

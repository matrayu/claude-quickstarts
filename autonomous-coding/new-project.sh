#!/bin/bash
# Quick project starter for autonomous coding agent

set -e

# Check arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <project-name> [feature-count] [max-iterations]"
    echo ""
    echo "Examples:"
    echo "  $0 my-todo-app              # Default: 200 features, unlimited iterations"
    echo "  $0 my-blog 50               # 50 features, unlimited iterations"
    echo "  $0 my-dashboard 30 5        # 30 features, max 5 iterations"
    echo ""
    exit 1
fi

PROJECT_NAME="$1"
FEATURE_COUNT="${2:-200}"
MAX_ITERATIONS="${3:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Starting autonomous coding agent for: $PROJECT_NAME"
echo "   Features: $FEATURE_COUNT"
echo "   Max iterations: ${MAX_ITERATIONS:-unlimited}"
echo ""

# Check API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ Error: ANTHROPIC_API_KEY not set"
    echo "   export ANTHROPIC_API_KEY='your-key-here'"
    exit 1
fi

# Activate virtual environment
cd "$SCRIPT_DIR"
source venv/bin/activate

# Build command
CMD="python autonomous_agent_demo.py --project-dir ./generations/$PROJECT_NAME"

if [ -n "$MAX_ITERATIONS" ]; then
    CMD="$CMD --max-iterations $MAX_ITERATIONS"
fi

echo "Running: $CMD"
echo ""
echo "💡 Tip: Press Ctrl+C to pause, run same command to resume"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run the agent
eval $CMD

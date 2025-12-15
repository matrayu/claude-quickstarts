#!/usr/bin/env python3
"""
Autonomous Coding Agent CLI
============================

A proper CLI tool for running autonomous coding agents anywhere.

Usage:
    autonomous-coding init      # Initialize project
    autonomous-coding start     # Start the agent
    autonomous-coding update    # Update the tool
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Optional

# Tool installation directory
TOOL_DIR = Path.home() / ".autonomous-coding-agent"
CONFIG_DIR_NAME = ".autonomous-coding"


def get_project_config_dir() -> Path:
    """Get the project config directory in current working directory."""
    return Path.cwd() / CONFIG_DIR_NAME


def init_command() -> None:
    """Initialize autonomous coding in current directory."""
    config_dir = get_project_config_dir()

    if config_dir.exists():
        print(f"❌ Already initialized in this directory")
        print(f"   Config found at: {config_dir}")
        response = input("Reinitialize? This will keep existing app_spec.txt (y/N): ")
        if response.lower() != 'y':
            return

    config_dir.mkdir(exist_ok=True)

    print("\n" + "="*70)
    print("  AUTONOMOUS CODING AGENT - PROJECT INITIALIZATION")
    print("="*70)
    print()

    # 1. App Spec
    app_spec_path = config_dir / "app_spec.txt"
    if app_spec_path.exists():
        print(f"✓ Existing app_spec.txt found")
        edit = input("Edit it now? (y/N): ")
        if edit.lower() == 'y':
            os.system(f"{os.environ.get('EDITOR', 'vim')} {app_spec_path}")
    else:
        print("\n1. APPLICATION SPECIFICATION")
        print("-" * 70)
        print("Choose an option:")
        print("  1. Create new app spec (interactive)")
        print("  2. Use example (Claude.ai clone)")
        print("  3. Provide path to existing spec")

        choice = input("\nChoice (1-3): ").strip()

        if choice == "1":
            create_interactive_spec(app_spec_path)
        elif choice == "2":
            copy_example_spec(app_spec_path)
        elif choice == "3":
            source_path = input("Path to app spec file: ").strip()
            if Path(source_path).exists():
                import shutil
                shutil.copy(source_path, app_spec_path)
                print(f"✓ Copied {source_path}")
            else:
                print(f"❌ File not found: {source_path}")
                return
        else:
            print("❌ Invalid choice")
            return

    # 2. Feature Count
    print("\n2. FEATURE COUNT")
    print("-" * 70)
    print("How many test cases should the agent generate?")
    print("  Recommendation: 20-50 for quick demos, 100-200 for full apps")

    while True:
        try:
            feature_count = int(input("Feature count (default 50): ").strip() or "50")
            if feature_count < 1:
                print("Must be at least 1")
                continue
            break
        except ValueError:
            print("Please enter a number")

    # 3. Model Selection
    print("\n3. MODEL SELECTION")
    print("-" * 70)
    print("Which Claude model to use?")
    print("  1. Claude Sonnet 4.5 (recommended, balanced)")
    print("  2. Claude Opus 4.5 (most capable, slower)")
    print("  3. Claude Haiku 4.5 (fastest, cheaper)")

    model_map = {
        "1": "claude-sonnet-4-5-20250929",
        "2": "claude-opus-4-5-20251101",
        "3": "claude-haiku-4-5-20251001",
    }

    model_choice = input("Choice (1-3, default 1): ").strip() or "1"
    model = model_map.get(model_choice, model_map["1"])

    # 4. API Key
    print("\n4. API KEY SETUP")
    print("-" * 70)

    if os.environ.get("ANTHROPIC_API_KEY"):
        print("✓ ANTHROPIC_API_KEY already set in environment")
        use_env = input("Use environment variable? (Y/n): ").strip().lower()
        if use_env != 'n':
            api_key_source = "environment"
        else:
            api_key = input("Enter API key: ").strip()
            api_key_source = "config"
    else:
        print("ANTHROPIC_API_KEY not found in environment")
        print("You can either:")
        print("  1. Set it now (will be saved in config)")
        print("  2. Set it as environment variable (recommended)")

        choice = input("Choice (1-2): ").strip()
        if choice == "1":
            api_key = input("Enter API key: ").strip()
            api_key_source = "config"
        else:
            print("\nAdd to your ~/.zshrc or ~/.bashrc:")
            print("  export ANTHROPIC_API_KEY='your-key-here'")
            print("\nThen source it: source ~/.zshrc")
            api_key_source = "environment"
            api_key = None

    # 5. Save Configuration
    config = {
        "feature_count": feature_count,
        "model": model,
        "api_key_source": api_key_source,
    }

    if api_key_source == "config" and 'api_key' in locals():
        config["api_key"] = api_key

    config_path = config_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    # 6. Create /tmp/api-key file
    if api_key_source == "config" and 'api_key' in locals():
        tmp_key_file = Path("/tmp/api-key")
        tmp_key_file.write_text(api_key)
        tmp_key_file.chmod(0o600)
    elif os.environ.get("ANTHROPIC_API_KEY"):
        tmp_key_file = Path("/tmp/api-key")
        tmp_key_file.write_text(os.environ["ANTHROPIC_API_KEY"])
        tmp_key_file.chmod(0o600)

    print("\n" + "="*70)
    print("  ✓ INITIALIZATION COMPLETE")
    print("="*70)
    print(f"\nConfiguration saved to: {config_dir}")
    print(f"  - App spec: {app_spec_path}")
    print(f"  - Config: {config_path}")
    print(f"  - Features: {feature_count}")
    print(f"  - Model: {model}")
    print()
    print("Next steps:")
    print("  1. Review/edit your app spec: vim .autonomous-coding/app_spec.txt")
    print("  2. Start the agent: autonomous-coding start")
    print()


def create_interactive_spec(output_path: Path) -> None:
    """Create app spec interactively."""
    print("\nLet's create your app specification!")
    print()

    app_name = input("App name: ").strip()
    app_description = input("Brief description: ").strip()

    print("\nTechnology stack:")
    frontend = input("  Frontend (e.g., React, Vue, Next.js): ").strip() or "React with Vite"
    backend = input("  Backend (e.g., Node.js, Python, Go): ").strip() or "Node.js with Express"
    database = input("  Database (e.g., PostgreSQL, SQLite, MongoDB): ").strip() or "SQLite"

    spec_content = f"""<project_specification>
  <project_name>{app_name}</project_name>

  <overview>
    {app_description}
  </overview>

  <technology_stack>
    <api_key>
      You can use an API key located at /tmp/api-key for testing.
    </api_key>
    <frontend>{frontend}</frontend>
    <backend>{backend}</backend>
    <database>{database}</database>
  </technology_stack>

  <core_features>
    <!-- Add your features here -->
    <feature_1>
      - Feature description
      - Implementation details
    </feature_1>
  </core_features>

  <success_criteria>
    <functionality>
      - List key functional requirements
    </functionality>
    <user_experience>
      - List UX requirements
    </user_experience>
  </success_criteria>
</project_specification>
"""

    output_path.write_text(spec_content)
    print(f"\n✓ Created {output_path}")

    edit = input("\nOpen in editor to add details? (Y/n): ").strip().lower()
    if edit != 'n':
        os.system(f"{os.environ.get('EDITOR', 'vim')} {output_path}")


def copy_example_spec(output_path: Path) -> None:
    """Copy example spec from tool directory."""
    example_path = TOOL_DIR / "prompts" / "app_spec.txt"
    if example_path.exists():
        import shutil
        shutil.copy(example_path, output_path)
        print(f"✓ Copied example spec to {output_path}")
    else:
        print(f"⚠ Example not found at {example_path}")
        print("Creating minimal template instead...")
        create_interactive_spec(output_path)


def start_command(max_iterations: Optional[int] = None) -> None:
    """Start the autonomous coding agent."""
    config_dir = get_project_config_dir()

    if not config_dir.exists():
        print("❌ Not initialized in this directory")
        print("   Run: autonomous-coding init")
        sys.exit(1)

    # Load config
    config_path = config_dir / "config.json"
    if not config_path.exists():
        print("❌ Config file not found")
        print(f"   Expected: {config_path}")
        sys.exit(1)

    with open(config_path) as f:
        config = json.load(f)

    # Set API key
    if config.get("api_key_source") == "config":
        os.environ["ANTHROPIC_API_KEY"] = config["api_key"]

    # Import and run the agent from the tool directory
    sys.path.insert(0, str(TOOL_DIR))

    from autonomous_agent_demo import run_autonomous_agent

    # Copy app spec to generations directory
    app_spec_source = config_dir / "app_spec.txt"
    project_dir = Path.cwd() / "generations" / Path.cwd().name
    project_dir.mkdir(parents=True, exist_ok=True)

    app_spec_dest = project_dir / "app_spec.txt"
    if not app_spec_dest.exists():
        import shutil
        shutil.copy(app_spec_source, app_spec_dest)

    # Update initializer prompt with feature count
    update_feature_count_in_prompts(config["feature_count"])

    # Run the agent
    asyncio.run(run_autonomous_agent(
        project_dir=project_dir,
        model=config["model"],
        max_iterations=max_iterations,
    ))


def update_feature_count_in_prompts(count: int) -> None:
    """Update feature count in initializer prompt template."""
    template_path = TOOL_DIR / "prompts" / "initializer_prompt.md"
    content = template_path.read_text()

    # Replace feature count
    import re
    content = re.sub(
        r'feature_list\.json` with \d+ detailed',
        f'feature_list.json` with {count} detailed',
        content
    )
    content = re.sub(
        r'Minimum \d+ features total',
        f'Minimum {count} features total',
        content
    )

    template_path.write_text(content)


def update_command() -> None:
    """Update the tool from the quickstarts repo."""
    print("Updating autonomous-coding-agent...")

    quickstart_dir = Path("/Users/206853553/Projects/personal/claude-quickstarts/autonomous-coding")

    if not quickstart_dir.exists():
        print(f"❌ Quickstart directory not found: {quickstart_dir}")
        print("   Update the path in the script or pull updates manually")
        return

    # Pull latest changes
    import subprocess
    result = subprocess.run(
        ["git", "pull"],
        cwd=quickstart_dir,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"⚠ Git pull failed: {result.stderr}")
    else:
        print("✓ Pulled latest changes")

    # Copy core files
    import shutil
    core_files = [
        "autonomous_agent_demo.py",
        "agent.py",
        "client.py",
        "security.py",
        "progress.py",
        "prompts.py",
        "requirements.txt",
    ]

    for file in core_files:
        src = quickstart_dir / file
        dst = TOOL_DIR / file
        if src.exists():
            shutil.copy(src, dst)
            print(f"  ✓ Updated {file}")

    # Copy prompts directory
    prompts_src = quickstart_dir / "prompts"
    prompts_dst = TOOL_DIR / "prompts"
    if prompts_src.exists():
        shutil.copytree(prompts_src, prompts_dst, dirs_exist_ok=True)
        print("  ✓ Updated prompts/")

    # Update venv
    venv_path = TOOL_DIR / "venv"
    if venv_path.exists():
        print("\n  Updating Python dependencies...")
        subprocess.run([
            str(venv_path / "bin" / "pip"),
            "install", "-r",
            str(TOOL_DIR / "requirements.txt")
        ])

    print("\n✓ Update complete!")
    print("  All projects will now use the updated tool")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Autonomous Coding Agent - Build complete applications with AI"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Init command
    subparsers.add_parser("init", help="Initialize project in current directory")

    # Start command
    start_parser = subparsers.add_parser("start", help="Start the coding agent")
    start_parser.add_argument(
        "--max-iterations",
        type=int,
        help="Maximum number of iterations"
    )

    # Update command
    subparsers.add_parser("update", help="Update the tool to latest version")

    args = parser.parse_args()

    if args.command == "init":
        init_command()
    elif args.command == "start":
        start_command(max_iterations=args.max_iterations)
    elif args.command == "update":
        update_command()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

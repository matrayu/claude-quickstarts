# Autonomous Coding Agent - Hardened Edition

## Implementation Plan

**Version:** 2.0  
**Status:** Draft  
**Primary Use Case:** Internal tool for solo power user  
**Core Improvements:**
- External verification layer to ensure output quality
- Tool management architecture for reliability
- Human checkpoints at critical decision points

---

## Executive Summary

This plan creates a production-hardened autonomous coding agent with three key architectural improvements over the demo:

1. **Verifier Agent** - Independent validation of every claimed test pass
2. **Tool Management** - Profile-based selection, error classification, resilient execution
3. **Human Checkpoints** - Strategic intervention points where your judgment matters most

The system optimizes for output quality over speed, with guardrails to prevent runaway costs.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ORCHESTRATOR                                   │
│                          (core/orchestrator.py)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌──────────────────┐    ┌─────────────────────────┐   │
│  │ INITIALIZER │───▶│  HUMAN REVIEW    │───▶│  CODING + VERIFICATION  │   │
│  │   AGENT     │    │  (feature list)  │    │        LOOP             │   │
│  └─────────────┘    └──────────────────┘    └─────────────────────────┘   │
│                                                      │                     │
│                              ┌───────────────────────┼───────────────┐     │
│                              ▼                       ▼               ▼     │
│                        ┌──────────┐           ┌──────────┐    ┌──────────┐│
│                        │  CODER   │──claims──▶│  GATES   │───▶│ VERIFIER ││
│                        │  AGENT   │           │          │    │  AGENT   ││
│                        └──────────┘           └──────────┘    └──────────┘│
│                              │                       │               │     │
│                              │                  fail │          fail │     │
│                              │                       ▼               ▼     │
│                              │              ┌─────────────────────────┐   │
│                              │              │      QUARANTINE         │   │
│                              │              │    (human review)       │   │
│                              │              └─────────────────────────┘   │
│                              │                                             │
├──────────────────────────────┼─────────────────────────────────────────────┤
│                              ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                        TOOL LAYER                                    │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │  │
│  │  │   TOOL      │  │   ERROR     │  │  RESILIENT  │  │   MCP      │ │  │
│  │  │  PROFILES   │  │ CLASSIFIER  │  │  EXECUTOR   │  │  SERVERS   │ │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                              ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                      TRACKING LAYER                                  │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐│  │
│  │  │  EVENTS  │  │  COSTS   │  │ PROGRESS │  │ VERIFICATION LOG     ││  │
│  │  │ (jsonl)  │  │  (json)  │  │  (json)  │  │ (json + screenshots) ││  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────────┘│  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
autonomous-coding-hardened/
├── README.md
├── requirements.txt
├── install.sh
│
├── cli.py                        # Main entry point
│
├── core/
│   ├── __init__.py
│   ├── orchestrator.py           # Main loop, session management
│   ├── client.py                 # Claude SDK client factory
│   ├── security.py               # Bash allowlist hooks
│   └── gates.py                  # Quality gate framework
│
├── agents/
│   ├── __init__.py
│   ├── initializer.py            # First-run agent logic
│   ├── coder.py                  # Implementation agent logic
│   └── verifier.py               # Verification agent logic
│
├── tools/
│   ├── __init__.py
│   ├── profiles.py               # Tool profiles by project type
│   ├── registry.py               # Available tools catalog
│   ├── errors.py                 # Error classification
│   ├── resilience.py             # Retry/fallback strategies
│   └── validation.py             # Pre-flight tool checks
│
├── prompts/
│   ├── initializer.md
│   ├── coder.md
│   └── verifier.md
│
├── tracking/
│   ├── __init__.py
│   ├── events.py                 # Structured event logging
│   ├── costs.py                  # Token usage tracking
│   └── progress.py               # Feature completion tracking
│
├── config/
│   ├── __init__.py
│   ├── settings.py               # Configuration management
│   └── defaults.yaml             # Default configuration values
│
└── generations/                  # Output projects land here
    └── [project-name]/
        ├── app_spec.txt
        ├── feature_list.json
        ├── .hardened/
        │   ├── config.yaml
        │   ├── costs.json
        │   ├── events.jsonl
        │   ├── verification_log.json
        │   ├── quarantine.json
        │   └── sessions/
        │       ├── session_001.json
        │       └── session_001_verify/
        │           └── screenshots/
        └── [generated app files]
```

---

## Phase 1: Foundation (Days 1-4)

### Goal
Core infrastructure: CLI, logging, cost tracking, configuration.

### Deliverables

#### 1.1 - CLI Entry Point (`cli.py`)

```bash
# Create new project
python cli.py new --spec ./my_spec.txt --name my-project --type web_app
python cli.py new --spec ./my_spec.txt --name my-project --detect-type

# Run agent
python cli.py run --project ./generations/my-project
python cli.py run --project ./generations/my-project --max-iterations 10

# Review feature list (required before coding begins)
python cli.py review --project ./generations/my-project

# Check status
python cli.py status --project ./generations/my-project

# View costs
python cli.py costs --project ./generations/my-project

# Review quarantined items
python cli.py quarantine --project ./generations/my-project

# Migrate from demo
python cli.py migrate --from ../autonomous-coding/generations/old-project
```

#### 1.2 - Event Logger (`tracking/events.py`)

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Literal
import json
from pathlib import Path

@dataclass
class AgentEvent:
    timestamp: datetime
    session_id: str
    agent_type: Literal["initializer", "coder", "verifier"]
    event_type: Literal[
        "session_start", 
        "session_end", 
        "tool_use", 
        "tool_error",
        "tool_retry",
        "claim", 
        "verification",
        "gate_pass",
        "gate_fail", 
        "quarantine",
        "error"
    ]
    data: dict
    
    def to_json(self) -> str:
        return json.dumps({
            "timestamp": self.timestamp.isoformat(),
            "session_id": self.session_id,
            "agent_type": self.agent_type,
            "event_type": self.event_type,
            "data": self.data,
        })

class EventLogger:
    def __init__(self, project_dir: Path):
        self.log_path = project_dir / ".hardened" / "events.jsonl"
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def log(self, event: AgentEvent) -> None:
        with open(self.log_path, "a") as f:
            f.write(event.to_json() + "\n")
    
    def get_events(
        self, 
        session_id: str = None, 
        event_type: str = None,
        since: datetime = None,
    ) -> list[AgentEvent]:
        """Query events with optional filters."""
        # Implementation: read jsonl, filter, return
        ...
```

#### 1.3 - Cost Tracker (`tracking/costs.py`)

```python
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

# Pricing per 1M tokens (as of 2025)
MODEL_PRICING = {
    "claude-sonnet-4-5-20250929": {"input": Decimal("3.00"), "output": Decimal("15.00")},
    "claude-haiku-4-5-20251001": {"input": Decimal("0.80"), "output": Decimal("4.00")},
}

@dataclass
class TokenUsage:
    session_id: str
    agent_type: str
    model: str
    input_tokens: int
    output_tokens: int
    timestamp: datetime
    
    @property
    def estimated_cost_usd(self) -> Decimal:
        pricing = MODEL_PRICING.get(self.model, MODEL_PRICING["claude-sonnet-4-5-20250929"])
        input_cost = (Decimal(self.input_tokens) / 1_000_000) * pricing["input"]
        output_cost = (Decimal(self.output_tokens) / 1_000_000) * pricing["output"]
        return input_cost + output_cost

class CostTracker:
    def __init__(self, project_dir: Path):
        self.costs_path = project_dir / ".hardened" / "costs.json"
        
    def record(self, usage: TokenUsage) -> None:
        """Append usage record."""
        ...
    
    def get_total_cost(self) -> Decimal:
        """Sum all recorded costs."""
        ...
    
    def get_cost_by_agent_type(self) -> dict[str, Decimal]:
        """Breakdown by agent type."""
        ...
    
    def get_cost_by_session(self) -> dict[str, Decimal]:
        """Breakdown by session."""
        ...
    
    def check_budget(self, limit: Decimal) -> BudgetStatus:
        """Check against budget limit."""
        total = self.get_total_cost()
        if total >= limit:
            return BudgetStatus.EXCEEDED
        elif total >= limit * Decimal("0.8"):
            return BudgetStatus.WARNING
        return BudgetStatus.OK
```

#### 1.4 - Configuration (`config/settings.py`)

```python
from dataclasses import dataclass, field
from pathlib import Path
from decimal import Decimal
import yaml

@dataclass
class ToolConfig:
    profile: str = "web_app"
    browser_timeout_ms: int = 30000
    max_retry_attempts: int = 3
    backoff_seconds: list[int] = field(default_factory=lambda: [1, 3, 10])
    screenshot_on_error: bool = True

@dataclass
class VerificationConfig:
    enabled: bool = True
    max_attempts: int = 2
    screenshot_each_step: bool = True
    adversarial_mode: bool = True  # Skeptical verifier prompt

@dataclass
class GatesConfig:
    lint: bool = True
    typecheck: bool = True
    build: bool = True
    smoke_test: bool = True
    lint_blocking: bool = True
    typecheck_blocking: bool = True
    build_blocking: bool = True
    smoke_test_blocking: bool = False

@dataclass 
class Config:
    # Model
    model: str = "claude-sonnet-4-5-20250929"
    verifier_model: str = "claude-sonnet-4-5-20250929"  # Could use cheaper model
    max_iterations: int | None = None
    
    # Timing
    continue_delay_seconds: int = 3
    verification_timeout_seconds: int = 300
    
    # Cost
    budget_limit_usd: Decimal = Decimal("100.00")
    budget_warning_threshold: Decimal = Decimal("0.8")
    
    # Test generation
    min_test_count: int = 40
    max_test_count: int = 150
    min_deep_test_ratio: float = 0.30  # 30% must have 8+ steps
    
    # Sub-configs
    tools: ToolConfig = field(default_factory=ToolConfig)
    verification: VerificationConfig = field(default_factory=VerificationConfig)
    gates: GatesConfig = field(default_factory=GatesConfig)
    
    @classmethod
    def load(cls, project_dir: Path) -> "Config":
        config_path = project_dir / ".hardened" / "config.yaml"
        if config_path.exists():
            with open(config_path) as f:
                data = yaml.safe_load(f)
            return cls(**data)
        return cls()
    
    def save(self, project_dir: Path) -> None:
        config_path = project_dir / ".hardened" / "config.yaml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            yaml.dump(self.__dict__, f, default_flow_style=False)
```

#### 1.5 - Basic Orchestrator Shell (`core/orchestrator.py`)

```python
async def run(project_dir: Path, config: Config) -> None:
    """Main orchestration loop."""
    
    logger = EventLogger(project_dir)
    costs = CostTracker(project_dir)
    
    # Validate tools before starting
    validation = await validate_tool_availability(project_dir, config)
    if not validation.valid:
        print("Tool validation failed:")
        for issue in validation.issues:
            print(f"  - {issue}")
        return
    
    # Check if initialization needed
    if is_first_run(project_dir):
        await run_initializer_session(project_dir, config, logger, costs)
        
        # HUMAN CHECKPOINT: Review feature list
        print("\n" + "=" * 70)
        print("  HUMAN REVIEW REQUIRED")
        print("=" * 70)
        print("\nInitialization complete. Review the feature list before continuing:")
        print(f"\n  python cli.py review --project {project_dir}")
        print("\nRun `python cli.py run` again after approval.")
        return
    
    # Check if feature list has been approved
    if not is_feature_list_approved(project_dir):
        print("Feature list not yet approved. Run:")
        print(f"\n  python cli.py review --project {project_dir}")
        return
    
    # Main coding loop
    iteration = 0
    while not is_complete(project_dir):
        iteration += 1
        
        # Check budget
        budget_status = costs.check_budget(config.budget_limit_usd)
        if budget_status == BudgetStatus.EXCEEDED:
            print(f"\nBudget limit (${config.budget_limit_usd}) exceeded. Stopping.")
            break
        elif budget_status == BudgetStatus.WARNING:
            print(f"\nWarning: Approaching budget limit (${config.budget_limit_usd})")
        
        # Check max iterations
        if config.max_iterations and iteration > config.max_iterations:
            print(f"\nMax iterations ({config.max_iterations}) reached.")
            break
        
        # Snapshot state before coder runs
        before_state = load_feature_list(project_dir)
        
        # Run coder session
        await run_coder_session(project_dir, config, logger, costs)
        
        # Extract claims
        after_state = load_feature_list(project_dir)
        claims = extract_claims(before_state, after_state)
        
        if not claims:
            # No new claims, continue
            await asyncio.sleep(config.continue_delay_seconds)
            continue
        
        # Run quality gates
        gate_results = await run_quality_gates(project_dir, config)
        blocking_failures = [r for r in gate_results if not r.passed and r.blocking]
        
        if blocking_failures:
            # Revert all claims, inject failures into next prompt
            for claim in claims:
                revert_claim(project_dir, claim.test_id)
            save_gate_failures(project_dir, blocking_failures)
            logger.log(AgentEvent(..., event_type="gate_fail", data={...}))
            await asyncio.sleep(config.continue_delay_seconds)
            continue
        
        # Verify each claim
        for claim in claims:
            result = await verify_claim_with_retry(
                project_dir, 
                claim, 
                config, 
                logger, 
                costs
            )
            
            if result == VerificationOutcome.CONFIRMED:
                logger.log(AgentEvent(..., event_type="verification", data={"result": "confirmed"}))
            
            elif result == VerificationOutcome.QUARANTINED:
                revert_claim(project_dir, claim.test_id)
                add_to_quarantine(project_dir, claim, result.evidence)
                logger.log(AgentEvent(..., event_type="quarantine", data={...}))
        
        # Print progress
        print_progress_summary(project_dir)
        
        # Check for quarantined items
        quarantine = load_quarantine(project_dir)
        if quarantine:
            print(f"\n⚠️  {len(quarantine)} items in quarantine. Review with:")
            print(f"   python cli.py quarantine --project {project_dir}")
        
        await asyncio.sleep(config.continue_delay_seconds)
    
    # Final summary
    print_final_summary(project_dir, costs)
```

### Exit Criteria - Phase 1
- [ ] CLI commands: `new`, `run`, `status`, `costs` working
- [ ] Events logged to `.hardened/events.jsonl`
- [ ] Costs tracked in `.hardened/costs.json`
- [ ] Configuration loads/saves from `.hardened/config.yaml`
- [ ] Budget checking halts on exceeded limit

---

## Phase 2: Tool Architecture (Days 5-8)

### Goal
Reliable tool execution with profiles, validation, and error handling.

### Deliverables

#### 2.1 - Tool Profiles (`tools/profiles.py`)

```python
from dataclasses import dataclass, field

@dataclass
class ToolProfile:
    name: str
    description: str
    required_tools: list[str]
    optional_tools: list[str]
    mcp_servers: dict[str, dict]
    bash_allowlist_additions: list[str] = field(default_factory=list)

TOOL_PROFILES = {
    "web_app": ToolProfile(
        name="web_app",
        description="Full-stack web application with UI",
        required_tools=["node", "npm"],
        optional_tools=["npx", "git"],
        mcp_servers={
            "playwright": {
                "command": "npx", 
                "args": ["-y", "@anthropic/mcp-playwright"]
            },
        },
        bash_allowlist_additions=["npx"],
    ),
    
    "api_backend": ToolProfile(
        name="api_backend",
        description="API/backend service without UI",
        required_tools=["node", "npm"],
        optional_tools=["curl", "git"],
        mcp_servers={},  # No browser automation
        bash_allowlist_additions=["curl"],
    ),
    
    "cli_tool": ToolProfile(
        name="cli_tool",
        description="Command-line application",
        required_tools=["node", "npm"],
        optional_tools=["git"],
        mcp_servers={},
    ),
    
    "static_site": ToolProfile(
        name="static_site",
        description="Static website with minimal interactivity",
        required_tools=["npm"],
        optional_tools=["npx", "git"],
        mcp_servers={
            "playwright": {
                "command": "npx",
                "args": ["-y", "@anthropic/mcp-playwright"]
            },
        },
    ),
    
    "python_app": ToolProfile(
        name="python_app", 
        description="Python application (CLI, API, or web)",
        required_tools=["python3", "pip"],
        optional_tools=["git", "pytest"],
        mcp_servers={
            "playwright": {
                "command": "npx",
                "args": ["-y", "@anthropic/mcp-playwright"]
            },
        },
        bash_allowlist_additions=["python3", "pip", "pytest"],
    ),
}

def detect_project_type(spec_text: str) -> str:
    """Analyze spec to determine project type."""
    
    spec_lower = spec_text.lower()
    
    signals = {
        "web_app": [
            ("react", 3), ("next.js", 3), ("frontend", 2), ("UI", 2),
            ("page", 1), ("button", 1), ("form", 1), ("CSS", 1),
            ("component", 2), ("dashboard", 2), ("login page", 2),
        ],
        "api_backend": [
            ("API", 2), ("endpoint", 3), ("REST", 3), ("GraphQL", 3),
            ("POST", 2), ("GET", 2), ("JSON response", 2), ("no frontend", 5),
            ("backend only", 5), ("microservice", 3),
        ],
        "cli_tool": [
            ("command line", 4), ("CLI", 4), ("terminal", 2),
            ("arguments", 2), ("flags", 2), ("--", 2), ("stdin", 3),
        ],
        "static_site": [
            ("landing page", 4), ("static", 3), ("no backend", 4),
            ("HTML only", 4), ("brochure", 3),
        ],
        "python_app": [
            ("python", 3), ("django", 4), ("flask", 4), ("fastapi", 4),
            ("pip", 2), (".py", 2),
        ],
    }
    
    scores = {ptype: 0 for ptype in signals}
    
    for ptype, keywords in signals.items():
        for keyword, weight in keywords:
            if keyword.lower() in spec_lower:
                scores[ptype] += weight
    
    # Default to web_app if no clear winner
    best = max(scores, key=scores.get)
    if scores[best] < 3:
        return "web_app"
    return best

def get_profile(project_type: str) -> ToolProfile:
    """Get tool profile, defaulting to web_app if unknown."""
    return TOOL_PROFILES.get(project_type, TOOL_PROFILES["web_app"])
```

#### 2.2 - Error Classification (`tools/errors.py`)

```python
from enum import Enum
from dataclasses import dataclass

class ToolErrorType(Enum):
    # Retriable
    TRANSIENT = "transient"         # Network timeout, rate limit
    TIMING = "timing"               # Element not found yet, page loading
    
    # Potentially recoverable
    SELECTOR = "selector"           # Element selector didn't match
    CAPABILITY = "capability"       # Tool can't do this specific action
    
    # Fatal
    NOT_INSTALLED = "not_installed" # Tool/server not available
    PERMISSION = "permission"       # Security blocked
    INVALID_INPUT = "invalid_input" # Malformed input

@dataclass
class ClassifiedError:
    error_type: ToolErrorType
    tool_name: str
    original_error: str
    hint: str | None = None

def classify_tool_error(tool_name: str, error: Exception) -> ClassifiedError:
    """Classify an error to determine handling strategy."""
    
    error_text = str(error).lower()
    
    # Transient (network/availability)
    transient_signals = [
        "timeout", "timed out", "rate limit", "429", "503", 
        "connection refused", "connection reset", "network",
        "temporarily unavailable", "retry"
    ]
    if any(s in error_text for s in transient_signals):
        return ClassifiedError(
            error_type=ToolErrorType.TRANSIENT,
            tool_name=tool_name,
            original_error=str(error),
            hint="Temporary failure. Will retry automatically."
        )
    
    # Timing (browser automation specific)
    timing_signals = [
        "waiting for selector", "element not found", "no element matches",
        "target closed", "page closed", "navigation timeout",
        "waiting for", "did not appear"
    ]
    if any(s in error_text for s in timing_signals):
        return ClassifiedError(
            error_type=ToolErrorType.TIMING,
            tool_name=tool_name,
            original_error=str(error),
            hint="Element not ready. Will retry with delay."
        )
    
    # Selector (element identification)
    selector_signals = [
        "selector", "locator", "multiple elements", "ambiguous",
        "strict mode violation", "resolved to", "matches"
    ]
    if any(s in error_text for s in selector_signals):
        return ClassifiedError(
            error_type=ToolErrorType.SELECTOR,
            tool_name=tool_name,
            original_error=str(error),
            hint=get_selector_hint(tool_name)
        )
    
    # Capability
    capability_signals = [
        "not supported", "not implemented", "cannot", "unable to",
        "doesn't support", "no such method", "invalid action"
    ]
    if any(s in error_text for s in capability_signals):
        return ClassifiedError(
            error_type=ToolErrorType.CAPABILITY,
            tool_name=tool_name,
            original_error=str(error),
            hint="This action may not be supported. Try alternative approach."
        )
    
    # Not installed
    install_signals = [
        "not found", "command not found", "no such file", "enoent",
        "spawn", "executable", "not recognized"
    ]
    if any(s in error_text for s in install_signals):
        return ClassifiedError(
            error_type=ToolErrorType.NOT_INSTALLED,
            tool_name=tool_name,
            original_error=str(error),
            hint=f"Tool '{tool_name}' may not be installed."
        )
    
    # Permission
    permission_signals = ["blocked", "denied", "permission", "not allowed", "forbidden"]
    if any(s in error_text for s in permission_signals):
        return ClassifiedError(
            error_type=ToolErrorType.PERMISSION,
            tool_name=tool_name,
            original_error=str(error),
            hint="Action blocked by security policy."
        )
    
    # Invalid input
    input_signals = [
        "invalid", "malformed", "expected", "required", "missing",
        "type error", "argument"
    ]
    if any(s in error_text for s in input_signals):
        return ClassifiedError(
            error_type=ToolErrorType.INVALID_INPUT,
            tool_name=tool_name,
            original_error=str(error),
            hint=get_usage_hint(tool_name)
        )
    
    # Default to transient (optimistic)
    return ClassifiedError(
        error_type=ToolErrorType.TRANSIENT,
        tool_name=tool_name,
        original_error=str(error),
        hint="Unknown error. Will retry."
    )

def get_selector_hint(tool_name: str) -> str:
    """Return helpful hint for selector failures."""
    
    if "playwright" in tool_name.lower():
        return """Selector failed. Try these approaches:
1. Use text selector: selector="text='Button Text'"
2. Use role selector: selector="button[name='submit']" 
3. Use test ID: selector="[data-testid='my-button']"
4. Use CSS with text: selector="button:has-text('Submit')"
5. First call playwright_get_visible_text to see what's on page"""
    
    if "puppeteer" in tool_name.lower():
        return """Selector failed. Try:
1. Use XPath: //button[contains(text(), 'Submit')]
2. Use data attributes: [data-testid='my-button']
3. First take screenshot to see current page state"""
    
    return "Selector did not match any elements. Verify element exists."

def get_usage_hint(tool_name: str) -> str:
    """Return usage hint for invalid input errors."""
    
    hints = {
        "playwright_click": "playwright_click requires 'selector' parameter",
        "playwright_fill": "playwright_fill requires 'selector' and 'value' parameters",
        "playwright_navigate": "playwright_navigate requires 'url' parameter",
        "playwright_screenshot": "playwright_screenshot optionally takes 'path' parameter",
    }
    
    return hints.get(tool_name, f"Check {tool_name} documentation for required parameters")
```

#### 2.3 - Resilient Executor (`tools/resilience.py`)

```python
from dataclasses import dataclass
from enum import Enum
import asyncio

class ExecutionOutcome(Enum):
    SUCCESS = "success"
    RETRY_EXHAUSTED = "retry_exhausted"
    FATAL = "fatal"
    NEEDS_HINT = "needs_hint"

@dataclass
class ToolResult:
    outcome: ExecutionOutcome
    data: dict | None = None
    error: str | None = None
    hint: str | None = None
    attempts: int = 1

@dataclass
class RetryConfig:
    max_attempts: int = 3
    backoff_seconds: list[int] = None
    
    def __post_init__(self):
        if self.backoff_seconds is None:
            self.backoff_seconds = [1, 3, 10]

# Strategies by error type
RETRY_STRATEGIES = {
    ToolErrorType.TRANSIENT: RetryConfig(max_attempts=3, backoff_seconds=[1, 3, 10]),
    ToolErrorType.TIMING: RetryConfig(max_attempts=3, backoff_seconds=[2, 5, 10]),
    ToolErrorType.SELECTOR: RetryConfig(max_attempts=1),  # Don't retry, needs hint
    ToolErrorType.CAPABILITY: RetryConfig(max_attempts=1),  # Don't retry
    ToolErrorType.NOT_INSTALLED: RetryConfig(max_attempts=1),  # Fatal
    ToolErrorType.PERMISSION: RetryConfig(max_attempts=1),  # Fatal
    ToolErrorType.INVALID_INPUT: RetryConfig(max_attempts=1),  # Needs hint
}

FATAL_ERROR_TYPES = {ToolErrorType.NOT_INSTALLED, ToolErrorType.PERMISSION}
HINT_ERROR_TYPES = {ToolErrorType.SELECTOR, ToolErrorType.INVALID_INPUT, ToolErrorType.CAPABILITY}

async def execute_with_resilience(
    tool_name: str,
    tool_input: dict,
    execute_fn,  # Actual tool execution function
    logger: EventLogger,
    config: RetryConfig = None,
) -> ToolResult:
    """Execute a tool with retry and error handling."""
    
    last_error = None
    attempt = 0
    
    while True:
        attempt += 1
        
        try:
            result = await execute_fn(tool_name, tool_input)
            return ToolResult(outcome=ExecutionOutcome.SUCCESS, data=result, attempts=attempt)
            
        except Exception as e:
            last_error = e
            classified = classify_tool_error(tool_name, e)
            
            # Log the error
            logger.log(AgentEvent(
                timestamp=datetime.now(),
                session_id="",  # Filled by caller
                agent_type="",  # Filled by caller
                event_type="tool_error",
                data={
                    "tool": tool_name,
                    "attempt": attempt,
                    "error_type": classified.error_type.value,
                    "error": str(e),
                }
            ))
            
            # Fatal errors - stop immediately
            if classified.error_type in FATAL_ERROR_TYPES:
                return ToolResult(
                    outcome=ExecutionOutcome.FATAL,
                    error=classified.original_error,
                    hint=classified.hint,
                    attempts=attempt,
                )
            
            # Hint errors - return hint to agent
            if classified.error_type in HINT_ERROR_TYPES:
                return ToolResult(
                    outcome=ExecutionOutcome.NEEDS_HINT,
                    error=classified.original_error,
                    hint=classified.hint,
                    attempts=attempt,
                )
            
            # Retriable errors - check retry budget
            strategy = config or RETRY_STRATEGIES.get(
                classified.error_type, 
                RetryConfig(max_attempts=1)
            )
            
            if attempt >= strategy.max_attempts:
                return ToolResult(
                    outcome=ExecutionOutcome.RETRY_EXHAUSTED,
                    error=f"Failed after {attempt} attempts: {classified.original_error}",
                    hint=classified.hint,
                    attempts=attempt,
                )
            
            # Wait and retry
            backoff_index = min(attempt - 1, len(strategy.backoff_seconds) - 1)
            wait_time = strategy.backoff_seconds[backoff_index]
            
            logger.log(AgentEvent(
                timestamp=datetime.now(),
                session_id="",
                agent_type="",
                event_type="tool_retry",
                data={
                    "tool": tool_name,
                    "attempt": attempt,
                    "next_attempt": attempt + 1,
                    "wait_seconds": wait_time,
                }
            ))
            
            await asyncio.sleep(wait_time)
```

#### 2.4 - Tool Validation (`tools/validation.py`)

```python
import shutil
import asyncio
from dataclasses import dataclass

@dataclass
class ValidationResult:
    valid: bool
    issues: list[str]
    warnings: list[str]

async def validate_tool_availability(
    project_dir: Path, 
    config: Config
) -> ValidationResult:
    """Pre-flight check that all required tools are available."""
    
    issues = []
    warnings = []
    
    profile = get_profile(config.tools.profile)
    
    # Check required bash tools
    for tool in profile.required_tools:
        if not shutil.which(tool):
            issues.append(f"Required tool '{tool}' not found in PATH")
    
    # Check optional bash tools
    for tool in profile.optional_tools:
        if not shutil.which(tool):
            warnings.append(f"Optional tool '{tool}' not found - some features may not work")
    
    # Check MCP servers can start
    for name, server_config in profile.mcp_servers.items():
        try:
            healthy = await check_mcp_server_health(server_config, timeout=15)
            if not healthy:
                issues.append(f"MCP server '{name}' failed health check")
        except Exception as e:
            issues.append(f"MCP server '{name}' failed to start: {e}")
    
    # Check for browser binaries if using browser automation
    if "playwright" in profile.mcp_servers:
        try:
            # Playwright should have browsers installed
            result = await asyncio.create_subprocess_exec(
                "npx", "playwright", "install", "--dry-run",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await result.wait()
            if result.returncode != 0:
                warnings.append("Playwright browsers may need installation: npx playwright install")
        except Exception:
            warnings.append("Could not verify Playwright browser installation")
    
    return ValidationResult(
        valid=len(issues) == 0,
        issues=issues,
        warnings=warnings,
    )

async def check_mcp_server_health(server_config: dict, timeout: int = 10) -> bool:
    """Attempt to start MCP server and verify it responds."""
    
    try:
        process = await asyncio.create_subprocess_exec(
            server_config["command"],
            *server_config["args"],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        # Give it a moment to start
        await asyncio.sleep(2)
        
        # Check if still running
        if process.returncode is not None:
            return False
        
        # Kill the test process
        process.terminate()
        await process.wait()
        
        return True
        
    except Exception:
        return False
```

### Exit Criteria - Phase 2
- [ ] Tool profiles defined for web_app, api_backend, cli_tool, static_site, python_app
- [ ] Project type auto-detection from spec working
- [ ] Error classification correctly categorizes common failures
- [ ] Retry logic with backoff working for transient errors
- [ ] Hints returned to agent for selector/input errors
- [ ] Pre-flight validation catches missing tools before run starts

---

## Phase 3: Verification System (Days 9-12)

### Goal
Independent verification that catches false "passing" claims.

### Deliverables

#### 3.1 - Verifier Prompt (`prompts/verifier.md`)

```markdown
## YOUR ROLE - VERIFICATION AGENT

You are an INDEPENDENT QUALITY GATE and a SKEPTICAL QA ENGINEER.

Your job is to FIND PROBLEMS, not confirm success. Assume the implementation 
is broken until proven otherwise.

You have NO knowledge of how features were implemented. You can only see:
1. The running application
2. The test steps to verify

### YOUR INPUTS

The application URL: {app_url}

The test case to verify:
```json
{test_case}
```

### YOUR TASK

Execute each step EXACTLY as written using browser automation tools.

For each step:
1. Perform the action described
2. Take a screenshot immediately after
3. Evaluate: did EXACTLY what was specified happen?

### CRITICAL EVALUATION CRITERIA

For each step, you must answer:
- Did exactly what was specified happen? (not "close enough")
- Would a real user consider this acceptable?
- Is there ANY way to interpret this as a failure?

**If you can construct a reasonable argument for failure, FAIL the test.**

Be strict about:
- Exact text matches (wrong capitalization = fail)
- Timing (if it says "within 2 seconds" and it took 3 = fail)
- Visual appearance (wrong color, cut off text, misaligned = fail)
- Completeness (if step says "verify X and Y" and only X works = fail)

### YOUR OUTPUT

Output ONLY this JSON structure, nothing else:

```json
{
  "test_passes": true | false,
  "steps": [
    {
      "step_number": 1,
      "step_text": "The step as written",
      "result": "pass" | "fail",
      "screenshot": "step_1.png",
      "observation": "What you actually observed",
      "reasoning": "Why this passes/fails the step criteria"
    }
  ],
  "overall_reasoning": "Summary of why the test passes or fails",
  "failure_reason": null | "Clear description of what failed and why"
}
```

### RULES

1. Execute steps LITERALLY - do not interpret, expand, or "help"
2. If ANY step fails, the entire test fails
3. If instructions are ambiguous, the test FAILS (implementation should be unambiguous)
4. Screenshots are MANDATORY for every step
5. No benefit of the doubt - this is production quality verification
6. Do not use JavaScript evaluation to bypass UI - test like a real user

### BROWSER AUTOMATION

Use Playwright tools:
- playwright_navigate - Go to URL
- playwright_click - Click elements (use text selectors: "text='Button Text'")
- playwright_fill - Fill form fields
- playwright_screenshot - Capture evidence
- playwright_get_visible_text - See what's on page if needed

Remember: You're testing what a USER would experience, not what the code does.
```

#### 3.2 - Verifier Agent (`agents/verifier.py`)

```python
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import json

class VerificationOutcome(Enum):
    CONFIRMED = "confirmed"
    FAILED = "failed"
    QUARANTINED = "quarantined"
    ERROR = "error"

@dataclass
class VerificationResult:
    outcome: VerificationOutcome
    test_id: int
    evidence_path: Path | None
    failure_reason: str | None
    raw_result: dict | None

async def run_verifier_session(
    project_dir: Path,
    test_case: dict,
    test_id: int,
    config: Config,
    logger: EventLogger,
    costs: CostTracker,
) -> VerificationResult:
    """Run verification for a single test case."""
    
    # Create evidence directory
    session_id = generate_session_id()
    evidence_dir = project_dir / ".hardened" / "sessions" / f"{session_id}_verify" / "screenshots"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    
    # Build prompt
    prompt = build_verifier_prompt(
        test_case=test_case,
        app_url=get_app_url(project_dir),
    )
    
    # Create client with limited tools (browser only)
    client = create_verifier_client(project_dir, config)
    
    logger.log(AgentEvent(
        timestamp=datetime.now(),
        session_id=session_id,
        agent_type="verifier",
        event_type="session_start",
        data={"test_id": test_id}
    ))
    
    try:
        async with client:
            response = await run_agent_session(client, prompt, project_dir)
        
        # Parse the JSON result
        result = parse_verification_response(response)
        
        # Record costs
        costs.record(TokenUsage(
            session_id=session_id,
            agent_type="verifier",
            model=config.verifier_model,
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
            timestamp=datetime.now(),
        ))
        
        if result and result.get("test_passes"):
            return VerificationResult(
                outcome=VerificationOutcome.CONFIRMED,
                test_id=test_id,
                evidence_path=evidence_dir,
                failure_reason=None,
                raw_result=result,
            )
        else:
            return VerificationResult(
                outcome=VerificationOutcome.FAILED,
                test_id=test_id,
                evidence_path=evidence_dir,
                failure_reason=result.get("failure_reason") if result else "Could not parse result",
                raw_result=result,
            )
    
    except Exception as e:
        logger.log(AgentEvent(
            timestamp=datetime.now(),
            session_id=session_id,
            agent_type="verifier",
            event_type="error",
            data={"error": str(e)}
        ))
        
        return VerificationResult(
            outcome=VerificationOutcome.ERROR,
            test_id=test_id,
            evidence_path=evidence_dir,
            failure_reason=str(e),
            raw_result=None,
        )

async def verify_claim_with_retry(
    project_dir: Path,
    claim: Claim,
    config: Config,
    logger: EventLogger,
    costs: CostTracker,
) -> VerificationOutcome:
    """Verify a claim with retry logic, quarantining on repeated failure."""
    
    for attempt in range(config.verification.max_attempts):
        result = await run_verifier_session(
            project_dir=project_dir,
            test_case=claim.test_case,
            test_id=claim.test_id,
            config=config,
            logger=logger,
            costs=costs,
        )
        
        if result.outcome == VerificationOutcome.CONFIRMED:
            return VerificationOutcome.CONFIRMED
        
        if result.outcome == VerificationOutcome.ERROR:
            # Transient error, retry
            if attempt < config.verification.max_attempts - 1:
                await asyncio.sleep(5)
                continue
        
        # Failed - if more attempts left, retry
        if attempt < config.verification.max_attempts - 1:
            await asyncio.sleep(5)
            continue
    
    # Exhausted retries - quarantine (don't auto-revert)
    return VerificationOutcome.QUARANTINED
```

#### 3.3 - Quarantine Management

```python
# In core/orchestrator.py

@dataclass
class QuarantineItem:
    test_id: int
    test_case: dict
    claimed_session: str
    verification_attempts: int
    failure_reasons: list[str]
    evidence_paths: list[Path]
    quarantined_at: datetime

def add_to_quarantine(
    project_dir: Path, 
    claim: Claim, 
    result: VerificationResult
) -> None:
    """Add a failed claim to quarantine for human review."""
    
    quarantine_path = project_dir / ".hardened" / "quarantine.json"
    
    if quarantine_path.exists():
        with open(quarantine_path) as f:
            quarantine = json.load(f)
    else:
        quarantine = []
    
    item = QuarantineItem(
        test_id=claim.test_id,
        test_case=claim.test_case,
        claimed_session=claim.session_id,
        verification_attempts=result.attempts if hasattr(result, 'attempts') else 1,
        failure_reasons=[result.failure_reason] if result.failure_reason else [],
        evidence_paths=[str(result.evidence_path)] if result.evidence_path else [],
        quarantined_at=datetime.now(),
    )
    
    quarantine.append(asdict(item))
    
    with open(quarantine_path, "w") as f:
        json.dump(quarantine, f, indent=2, default=str)

# CLI command for quarantine review
def cmd_quarantine(project_dir: Path) -> None:
    """Review quarantined items."""
    
    quarantine_path = project_dir / ".hardened" / "quarantine.json"
    
    if not quarantine_path.exists():
        print("No items in quarantine.")
        return
    
    with open(quarantine_path) as f:
        quarantine = json.load(f)
    
    if not quarantine:
        print("No items in quarantine.")
        return
    
    print(f"\n{'=' * 70}")
    print(f"  QUARANTINE REVIEW: {len(quarantine)} items")
    print(f"{'=' * 70}")
    
    for i, item in enumerate(quarantine, 1):
        print(f"\n[{i}] Test #{item['test_id']}: {item['test_case']['description'][:50]}...")
        print(f"    Failure: {item['failure_reasons'][0] if item['failure_reasons'] else 'Unknown'}")
        print(f"    Evidence: {item['evidence_paths'][0] if item['evidence_paths'] else 'None'}")
        print(f"    Quarantined: {item['quarantined_at']}")
    
    print(f"\n{'=' * 70}")
    print("Options:")
    print("  python cli.py quarantine --project ... --approve <number>")
    print("  python cli.py quarantine --project ... --reject <number>")
    print("  python cli.py quarantine --project ... --view <number>")
    print(f"{'=' * 70}")
```

### Exit Criteria - Phase 3
- [ ] Verifier agent runs with adversarial prompt
- [ ] Claims extracted from before/after feature_list.json diff
- [ ] Verification retries on transient failures
- [ ] Failed verifications quarantined (not auto-reverted)
- [ ] Screenshots saved as evidence
- [ ] `cli.py quarantine` command shows pending items
- [ ] Can approve/reject quarantined items

---

## Phase 4: Quality Gates (Days 13-14)

### Goal
Automated checks that block progression on objective criteria.

### Deliverables

#### 4.1 - Gate Framework (`core/gates.py`)

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
import asyncio

@dataclass
class GateResult:
    gate_name: str
    passed: bool
    blocking: bool
    message: str
    details: dict | None = None

class QualityGate(ABC):
    name: str
    blocking: bool = True
    
    @abstractmethod
    async def check(self, project_dir: Path) -> GateResult:
        pass

class LintGate(QualityGate):
    name = "lint"
    
    async def check(self, project_dir: Path) -> GateResult:
        result = await asyncio.create_subprocess_exec(
            "npm", "run", "lint",
            cwd=project_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await result.communicate()
        
        return GateResult(
            gate_name=self.name,
            passed=result.returncode == 0,
            blocking=self.blocking,
            message="Lint passed" if result.returncode == 0 else "Lint errors found",
            details={"stdout": stdout.decode(), "stderr": stderr.decode()},
        )

class TypeCheckGate(QualityGate):
    name = "typecheck"
    
    async def check(self, project_dir: Path) -> GateResult:
        # Check if TypeScript project
        if not (project_dir / "tsconfig.json").exists():
            return GateResult(
                gate_name=self.name,
                passed=True,
                blocking=False,
                message="Not a TypeScript project, skipping",
            )
        
        result = await asyncio.create_subprocess_exec(
            "npx", "tsc", "--noEmit",
            cwd=project_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await result.communicate()
        
        return GateResult(
            gate_name=self.name,
            passed=result.returncode == 0,
            blocking=self.blocking,
            message="Type check passed" if result.returncode == 0 else "Type errors found",
            details={"stdout": stdout.decode(), "stderr": stderr.decode()},
        )

class BuildGate(QualityGate):
    name = "build"
    
    async def check(self, project_dir: Path) -> GateResult:
        result = await asyncio.create_subprocess_exec(
            "npm", "run", "build",
            cwd=project_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await result.communicate()
        
        return GateResult(
            gate_name=self.name,
            passed=result.returncode == 0,
            blocking=self.blocking,
            message="Build succeeded" if result.returncode == 0 else "Build failed",
            details={"stdout": stdout.decode(), "stderr": stderr.decode()},
        )

class SmokeTestGate(QualityGate):
    """Verify the app actually loads and renders."""
    name = "smoke_test"
    blocking = False  # Warning only by default
    
    async def check(self, project_dir: Path) -> GateResult:
        app_url = get_app_url(project_dir)
        
        try:
            # Use playwright to load the app
            # This is simplified - actual implementation would use MCP
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                # Navigate with timeout
                response = await page.goto(app_url, timeout=30000)
                
                # Check response
                if not response or response.status >= 400:
                    return GateResult(
                        gate_name=self.name,
                        passed=False,
                        blocking=self.blocking,
                        message=f"App returned HTTP {response.status if response else 'no response'}",
                    )
                
                # Check for console errors
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(2)  # Let any JS errors surface
                
                # Check for visible content
                content = await page.content()
                if len(content) < 100:
                    return GateResult(
                        gate_name=self.name,
                        passed=False,
                        blocking=self.blocking,
                        message="App rendered but page appears empty",
                    )
                
                await browser.close()
                
                if errors:
                    return GateResult(
                        gate_name=self.name,
                        passed=False,
                        blocking=self.blocking,
                        message=f"App has {len(errors)} console error(s)",
                        details={"errors": errors[:5]},  # First 5
                    )
                
                return GateResult(
                    gate_name=self.name,
                    passed=True,
                    blocking=self.blocking,
                    message="App loads and renders without errors",
                )
        
        except Exception as e:
            return GateResult(
                gate_name=self.name,
                passed=False,
                blocking=self.blocking,
                message=f"Smoke test failed: {e}",
            )

async def run_quality_gates(project_dir: Path, config: GatesConfig) -> list[GateResult]:
    """Run all enabled quality gates."""
    
    gates = []
    
    if config.lint:
        gate = LintGate()
        gate.blocking = config.lint_blocking
        gates.append(gate)
    
    if config.typecheck:
        gate = TypeCheckGate()
        gate.blocking = config.typecheck_blocking
        gates.append(gate)
    
    if config.build:
        gate = BuildGate()
        gate.blocking = config.build_blocking
        gates.append(gate)
    
    if config.smoke_test:
        gate = SmokeTestGate()
        gate.blocking = config.smoke_test_blocking
        gates.append(gate)
    
    results = []
    for gate in gates:
        result = await gate.check(project_dir)
        results.append(result)
        
        # Log result
        status = "✓" if result.passed else ("✗ BLOCKING" if result.blocking else "⚠ WARNING")
        print(f"  {status} {result.gate_name}: {result.message}")
    
    return results
```

### Exit Criteria - Phase 4
- [ ] Lint, typecheck, build gates implemented
- [ ] Smoke test gate loads app and checks for errors
- [ ] Blocking gates prevent verification from running
- [ ] Gate failures injected into next coder prompt
- [ ] Non-blocking gates logged as warnings

---

## Phase 5: Prompts & Human Checkpoints (Days 15-16)

### Goal
Refined prompts and human review integration.

### Deliverables

#### 5.1 - Updated Initializer Prompt (`prompts/initializer.md`)

```markdown
## YOUR ROLE - INITIALIZER AGENT (Session 1 of Many)

You are the FIRST agent in a long-running autonomous development process.
Your job is to set up the foundation for all future coding agents.

### FIRST: Read the Project Specification

Read `app_spec.txt` in your working directory. This contains the complete 
specification for what you need to build.

### SECOND: Calculate Test Count

Before generating tests, analyze the spec and calculate your target:

1. Count spec sections/features: ___ × 4 tests = ___
2. Count user roles: ___ × 6 tests = ___  
3. Count external integrations: ___ × 4 tests = ___
4. Count distinct UI components: ___ × 2 style tests = ___
5. Sum = ___

Apply bounds:
- Minimum: 40 tests (even for simple specs)
- Maximum: 150 tests (even for complex specs)
- Final target: [your calculated number]

State your calculation before generating feature_list.json.

### THIRD: Create feature_list.json

Generate tests following these requirements:

**Composition:**
- 60% functional tests (features work correctly)
- 25% edge case tests (error handling, invalid input)
- 15% style tests (visual appearance, UX)

**Depth requirements:**
- Minimum 4 steps per test (no trivial tests)
- At least 30% must have 8+ steps (deep user journeys)

**Step quality requirements:**

Each step MUST be:
- **Observable**: Describes what you SEE, not internal behavior
- **Specific**: Includes exact text, selectors, or measurable criteria
- **Atomic**: One action, one verification per step
- **Unambiguous**: A skeptical verifier can evaluate pass/fail

BAD step: "Verify message appears"
GOOD step: "Verify message 'Hello world' appears in element with 
            data-testid='chat-message', with timestamp showing current 
            time (±1 minute), sender name 'TestUser' displayed above"

BAD test: Single test for "messaging works"
GOOD tests: Separate tests for:
  - Send empty message (should show error)
  - Send 1000-char message (should truncate or work)
  - Send message with <script> tag (should sanitize)
  - Send message and refresh page (should persist)

**Format:**
```json
[
  {
    "id": 1,
    "category": "functional",
    "description": "Brief description",
    "steps": [
      "Step 1: Navigate to...",
      "Step 2: Click button with text 'Submit'",
      "Step 3: Verify element [data-testid='result'] contains 'Success'"
    ],
    "passes": false
  }
]
```

### FOURTH: Create init.sh

Create a setup script that:
1. Installs dependencies
2. Starts development server
3. Prints the URL to access the app

### FIFTH: Initialize Git

```bash
git init
git add .
git commit -m "Initial setup: feature_list.json, init.sh, project structure"
```

### SIXTH: Create Project Structure

Set up directories based on the tech stack in app_spec.txt.

### ENDING THIS SESSION

Before finishing:
1. Ensure feature_list.json has your calculated number of tests
2. Verify at least 30% of tests have 8+ steps
3. Commit all work
4. Create claude-progress.txt summarizing what you set up

**IMPORTANT:** After this session, a human will review feature_list.json 
before coding begins. Make sure your tests are specific and verifiable.
```

#### 5.2 - Human Review Command

```python
# In cli.py

def cmd_review(project_dir: Path) -> None:
    """Interactive review of feature list before coding begins."""
    
    feature_list_path = project_dir / "feature_list.json"
    approval_path = project_dir / ".hardened" / "feature_list_approved"
    
    if not feature_list_path.exists():
        print("No feature_list.json found. Run initialization first.")
        return
    
    with open(feature_list_path) as f:
        features = json.load(f)
    
    # Calculate stats
    total = len(features)
    functional = len([f for f in features if f.get("category") == "functional"])
    edge_cases = len([f for f in features if "edge" in f.get("category", "").lower() or "error" in f.get("description", "").lower()])
    style = len([f for f in features if f.get("category") == "style"])
    deep_tests = len([f for f in features if len(f.get("steps", [])) >= 8])
    avg_steps = sum(len(f.get("steps", [])) for f in features) / total if total else 0
    
    print(f"\n{'=' * 70}")
    print(f"  FEATURE LIST REVIEW")
    print(f"{'=' * 70}")
    print(f"\n  Project: {project_dir.name}")
    print(f"\n  STATISTICS:")
    print(f"    Total tests:        {total}")
    print(f"    Functional:         {functional} ({functional/total*100:.0f}%)")
    print(f"    Edge cases:         {edge_cases} ({edge_cases/total*100:.0f}%)")
    print(f"    Style:              {style} ({style/total*100:.0f}%)")
    print(f"    Deep tests (8+):    {deep_tests} ({deep_tests/total*100:.0f}%)")
    print(f"    Avg steps/test:     {avg_steps:.1f}")
    
    # Warnings
    warnings = []
    if total < 40:
        warnings.append(f"Below minimum test count (40). Have {total}.")
    if total > 150:
        warnings.append(f"Above maximum test count (150). Have {total}.")
    if deep_tests / total < 0.30:
        warnings.append(f"Deep test ratio below 30%. Have {deep_tests/total*100:.0f}%.")
    if avg_steps < 4:
        warnings.append(f"Average steps too low. Have {avg_steps:.1f}, want 4+.")
    
    if warnings:
        print(f"\n  ⚠️  WARNINGS:")
        for w in warnings:
            print(f"    - {w}")
    
    # Sample tests
    print(f"\n  SAMPLE TESTS:")
    for i, feature in enumerate(features[:3], 1):
        print(f"\n  [{i}] {feature.get('description', 'No description')[:60]}...")
        steps = feature.get("steps", [])
        for j, step in enumerate(steps[:3], 1):
            print(f"      Step {j}: {step[:50]}...")
        if len(steps) > 3:
            print(f"      ... and {len(steps) - 3} more steps")
    
    print(f"\n{'=' * 70}")
    print("  OPTIONS:")
    print("    [a] Approve and continue to coding")
    print("    [e] Open feature_list.json in editor")
    print("    [v] View all tests")
    print("    [q] Quit without approving")
    print(f"{'=' * 70}")
    
    choice = input("\n  Your choice: ").strip().lower()
    
    if choice == 'a':
        approval_path.parent.mkdir(parents=True, exist_ok=True)
        approval_path.write_text(datetime.now().isoformat())
        print("\n  ✓ Feature list approved. Run `python cli.py run` to start coding.")
    elif choice == 'e':
        import subprocess
        editor = os.environ.get("EDITOR", "vim")
        subprocess.run([editor, str(feature_list_path)])
        print("\n  File edited. Run `python cli.py review` again to approve.")
    elif choice == 'v':
        for i, feature in enumerate(features, 1):
            print(f"\n[{i}] {feature.get('description')}")
            for j, step in enumerate(feature.get("steps", []), 1):
                print(f"    {j}. {step}")
    else:
        print("\n  Review cancelled.")
```

### Exit Criteria - Phase 5
- [ ] Initializer prompt includes test count calculation
- [ ] Initializer prompt has step quality requirements
- [ ] `cli.py review` shows statistics and warnings
- [ ] Approval gate blocks coding until human approves
- [ ] Can edit feature_list.json and re-review

---

## Phase 6: Observability (Days 17-18, Optional)

### Goal
Visibility into agent progress without watching terminal.

### Deliverables

#### 6.1 - Status Dashboard (`cli.py status`)

```
$ python cli.py status --project ./generations/my-project

╔══════════════════════════════════════════════════════════════════════╗
║  PROJECT: my-project                                                  ║
║  Type: web_app | Model: claude-sonnet-4-5                            ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  PROGRESS                                                             ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━░░░░░░░░░░  72/150 (48%)    ║
║                                                                       ║
║  By category:                                                         ║
║    Functional:  45/90  (50%)                                         ║
║    Edge cases:  18/38  (47%)                                         ║
║    Style:        9/22  (41%)                                         ║
║                                                                       ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  SESSIONS                                                             ║
║    Completed:     28 (12 coder, 16 verifier)                         ║
║    Total runtime: 6h 42m                                             ║
║                                                                       ║
║  LAST SESSION: #28 (Verifier) - 12 min ago                           ║
║    Verified test #73: "User can reset password"                      ║
║    Result: CONFIRMED                                                  ║
║                                                                       ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  COSTS                                                                ║
║    Total:        $34.82                                               ║
║    Budget:       $100.00 (34.8% used)                                ║
║    By agent:     Coder $22.14 | Verifier $12.68                      ║
║    Per test:     $0.48 avg                                           ║
║                                                                       ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  QUALITY GATES                                                        ║
║    ✓ lint          ✓ typecheck       ✓ build       ✓ smoke_test     ║
║                                                                       ║
║  QUARANTINE: 2 items pending review                                  ║
║    Run: python cli.py quarantine --project ./generations/my-project  ║
║                                                                       ║
╚══════════════════════════════════════════════════════════════════════╝
```

#### 6.2 - Webhook Notifications (Optional)

```python
# In config
webhooks:
  on_test_pass: "https://hooks.slack.com/..."
  on_verification_fail: "https://hooks.slack.com/..."
  on_gate_fail: "https://hooks.slack.com/..."
  on_budget_warning: "https://hooks.slack.com/..."
  on_complete: "https://hooks.slack.com/..."
```

### Exit Criteria - Phase 6
- [ ] `cli.py status` shows comprehensive dashboard
- [ ] Progress bar with category breakdown
- [ ] Cost tracking with per-test averages
- [ ] Webhook notifications (if configured)

---

## Timeline Summary

| Phase | Days | Focus | Key Deliverable |
|-------|------|-------|-----------------|
| 1 - Foundation | 1-4 | CLI, logging, config | Basic orchestration working |
| 2 - Tools | 5-8 | Profiles, resilience | Reliable tool execution |
| 3 - Verification | 9-12 | Verifier agent, quarantine | Independent quality validation |
| 4 - Gates | 13-14 | Quality checks | Automated blocking gates |
| 5 - Prompts | 15-16 | Refined prompts, human review | Human checkpoint integration |
| 6 - Observability | 17-18 | Status, webhooks | Visibility dashboard |

**Total: 16-18 days to production-hardened system**

---

## Success Metrics

After Phase 3 (Verification), measure:

1. **Revert rate** - What % of coder claims fail verification?
   - Target: < 20% (indicates good coder prompt)
   - If > 40%: Coder prompt needs work

2. **Quarantine rate** - What % of claims go to quarantine?
   - Target: < 10%
   - High rate may indicate flaky verification

3. **Cost per verified test** - Total cost / confirmed tests
   - Baseline: Measure first 20 tests
   - Should decrease over time

4. **Human intervention rate** - How often you review quarantine
   - Target: < 5% of tests need manual review

---

## Configuration Reference

### Full `.hardened/config.yaml`

```yaml
# Model settings
model: claude-sonnet-4-5-20250929
verifier_model: claude-sonnet-4-5-20250929
max_iterations: null

# Timing
continue_delay_seconds: 3
verification_timeout_seconds: 300

# Cost controls
budget_limit_usd: 100.00
budget_warning_threshold: 0.8

# Test generation
min_test_count: 40
max_test_count: 150
min_deep_test_ratio: 0.30

# Tools
tools:
  profile: web_app
  browser_timeout_ms: 30000
  max_retry_attempts: 3
  backoff_seconds: [1, 3, 10]
  screenshot_on_error: true

# Verification
verification:
  enabled: true
  max_attempts: 2
  screenshot_each_step: true
  adversarial_mode: true

# Quality gates
gates:
  lint: true
  lint_blocking: true
  typecheck: true
  typecheck_blocking: true
  build: true
  build_blocking: true
  smoke_test: true
  smoke_test_blocking: false

# Notifications (optional)
webhooks:
  on_test_pass: null
  on_verification_fail: null
  on_gate_fail: null
  on_budget_warning: null
  on_complete: null
```

---

## Next Steps

1. Review this updated plan
2. Confirm scope (all 6 phases, or stop at Phase 5?)
3. Begin Phase 1 implementation

---

*Document version: 2.0 | Updated with tool architecture and assumption mitigations*

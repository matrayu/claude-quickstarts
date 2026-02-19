# Customization Example: Add Code Review Gate

## Inspired by `/agents`, implemented in `autonomous-coding`

### 1. Study the Pattern from /agents

```python
# From agents/tools/base.py - shows how to create tools
class Tool:
    name: str
    description: str

    def execute(self, **kwargs):
        # Your tool logic
        pass
```

### 2. Create Custom Tool for autonomous-coding

```python
# Create: autonomous-coding/custom_tools/code_review.py

from claude_code_sdk.types import Tool

class CodeReviewTool:
    """Gate that requires code review before continuing."""

    @staticmethod
    def to_dict():
        return {
            "name": "request_code_review",
            "description": "Request human code review before continuing",
            "input_schema": {
                "type": "object",
                "properties": {
                    "files_changed": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of files that were modified"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Why review is needed"
                    }
                },
                "required": ["files_changed", "reason"]
            }
        }

    @staticmethod
    def execute(files_changed, reason):
        print(f"\n{'='*70}")
        print("  CODE REVIEW REQUIRED")
        print(f"{'='*70}")
        print(f"\nReason: {reason}")
        print(f"\nFiles changed:")
        for f in files_changed:
            print(f"  - {f}")
        print("\nReview the code, then:")
        print("  APPROVE: Press Enter to continue")
        print("  REJECT: Type 'reject' to stop")

        response = input("\nYour decision: ").strip().lower()

        if response == "reject":
            return {"approved": False, "message": "Human rejected changes"}
        else:
            return {"approved": True, "message": "Human approved changes"}
```

### 3. Add to autonomous-coding

```python
# In client.py, add to system prompt:

system_prompt="""You are an expert full-stack developer.

IMPORTANT: Before committing significant changes, you MUST:
1. Use the request_code_review tool
2. List all files you modified
3. Wait for human approval

Only continue after approval."""

# Add to allowed tools:
allowed_tools=[
    *BUILTIN_TOOLS,
    *PLAYWRIGHT_TOOLS,
    "request_code_review",  # Your custom tool
]
```

### 4. Implement the Hook

```python
# In client.py, add to hooks:

from custom_tools.code_review import CodeReviewTool

hooks={
    "PreToolUse": [
        HookMatcher(matcher="Bash", hooks=[bash_security_hook]),
    ],
    "ToolExecution": [
        HookMatcher(
            matcher="request_code_review",
            hooks=[CodeReviewTool.execute]
        ),
    ],
}
```

### 5. Update the Coding Prompt

```python
# In prompts/coding_prompt.md, add:

## Code Review Process

Before committing major changes:
1. Call request_code_review with:
   - List of files you modified
   - Brief explanation of changes
2. Wait for approval
3. Only proceed if approved
```

## Result

Now the agent will:
1. Implement a feature
2. Request human review
3. Wait for your approval
4. Only continue if you approve

This pattern from `/agents` (custom tools) is adapted to the `autonomous-coding` framework (Claude Agent SDK).

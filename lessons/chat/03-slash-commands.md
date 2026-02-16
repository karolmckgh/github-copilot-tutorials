# Lesson 3: Slash Commands

> **XP:** 25 | **Difficulty:** Beginner | **Time:** 15 minutes

## Learning Objectives

By the end of this lesson, you will:
- Know the available slash commands in Copilot Chat
- Understand when to use each command
- Practice using them on real code

---

## What are Slash Commands?

Slash commands are **shortcuts** for common tasks in GitHub Copilot Chat. Instead of typing out detailed prompts, you can use a simple command to perform frequent operations.

Think of them as keyboard shortcuts for your AI assistant—quick, memorable, and efficient.

### Why Use Slash Commands?

1. **Speed** - Faster than typing full prompts
2. **Consistency** - Produces predictable results
3. **Discoverability** - Easy to remember and find
4. **Context-aware** - Works with selected code automatically

---

## Command Reference

| Command | Purpose | Example Use Case |
|---------|---------|------------------|
| `/explain` | Explain selected code | Understanding unfamiliar code |
| `/fix` | Fix bugs or issues | Resolving errors in your code |
| `/tests` | Generate unit tests | Creating test coverage |
| `/clear` | Clear chat history | Starting a fresh conversation |

### How to Use

1. Select code in your editor (optional for some commands)
2. Open Copilot Chat (`Ctrl+Shift+I` or `Cmd+Shift+I`)
3. Type the slash command
4. Press Enter

---

## Deep Dive: /tests

The `/tests` command is arguably the **most useful** slash command for developers. It generates unit tests for selected code.

### Basic Usage

1. Select a function in your editor
2. Type `/tests` in Copilot Chat
3. Review and apply the generated tests

### Example

Given this Python function:

```python
def calculate_shipping(weight, distance, express=False):
    base_rate = 5.0
    weight_rate = 0.5 * weight
    distance_rate = 0.1 * distance
    total = base_rate + weight_rate + distance_rate
    if express:
        total *= 1.5
    return round(total, 2)
```

Using `/tests` might generate:

```python
import pytest
from shipping import calculate_shipping

def test_calculate_shipping_basic():
    result = calculate_shipping(10, 100)
    assert result == 20.0  # 5 + 5 + 10

def test_calculate_shipping_express():
    result = calculate_shipping(10, 100, express=True)
    assert result == 30.0  # (5 + 5 + 10) * 1.5

def test_calculate_shipping_zero_weight():
    result = calculate_shipping(0, 100)
    assert result == 15.0  # 5 + 0 + 10

def test_calculate_shipping_zero_distance():
    result = calculate_shipping(10, 0)
    assert result == 10.0  # 5 + 5 + 0
```

### Tips for Better Tests

- **Select specific functions** rather than entire files
- **Add context**: `/tests using pytest with edge cases`
- **Specify framework**: `/tests using jest` or `/tests using unittest`

---

## Other Useful Commands

### /explain

Perfect for understanding unfamiliar code:

```
/explain
```

Copilot will break down:
- What the code does
- How it works step by step
- Any important patterns or concepts

### /fix

When you have code with errors:

```
/fix
```

Copilot will:
- Identify the issue
- Explain what's wrong
- Provide a corrected version

### /clear

Start fresh when the conversation gets cluttered:

```
/clear
```

This resets the chat context—useful when switching tasks.

---

## Exercise: Generate Tests

### Your Task

Use `/tests` on the sample code below and save your result.

### Sample Code

```python
def calculate_shipping(weight, distance, express=False):
    base_rate = 5.0
    weight_rate = 0.5 * weight
    distance_rate = 0.1 * distance
    total = base_rate + weight_rate + distance_rate
    if express:
        total *= 1.5
    return round(total, 2)
```

### Steps

1. Copy the sample code to a new file
2. Select the function
3. Open Copilot Chat and type `/tests`
4. Review the generated tests — when you're happy, say **"verify"** and Copilot will save them for you!

### Bonus Challenges

- Try `/tests using pytest with edge cases for invalid inputs`
- Generate tests in a different language (JavaScript)

---

## Verification

To complete this lesson, say **"verify"**. Copilot will:
1. Find the tests you generated in the conversation
2. Save them to `exercises/chat/03-tests.py` (or `.js`)
3. Award your XP!

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────┐
│           COPILOT CHAT SLASH COMMANDS           │
├─────────────────────────────────────────────────┤
│  /explain  →  Understand code                   │
│  /fix      →  Fix bugs and errors               │
│  /tests    →  Generate unit tests               │
│  /clear    →  Reset chat history                │
├─────────────────────────────────────────────────┤
│  Pro Tips:                                      │
│  • Select code first for context                │
│  • Add details: /tests using jest               │
│  • Combine: /tests with edge cases              │
└─────────────────────────────────────────────────┘
```

---

## Summary

| Command | When to Use |
|---------|-------------|
| `/explain` | Understanding new/complex code |
| `/fix` | Debugging errors |
| `/tests` | Building test coverage |
| `/clear` | Starting fresh |

**Key Takeaway:** Slash commands are your productivity shortcuts. Master `/tests` first—it'll save you the most time!

---

## Next Steps

Continue to [Lesson 4: Chat Participants](./04-participants.md) to learn about @workspace, @terminal, and other context providers.

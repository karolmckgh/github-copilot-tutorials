# Lesson 7: Fleet Agents

**XP: 75** | **Difficulty: Intermediate** | **Time: 15 minutes**

---

## 🎯 Learning Objectives

By the end of this lesson, you will:
- Understand when a task needs fleet mode vs. regular agentic mode
- Use `/fleet` to delegate work to parallel subagents
- Design tasks for maximum parallelism using a shared pattern approach
- Build a multi-feature app in minutes using only HTML & CSS

---

## 🚀 From Single Agent to Fleet

In Lesson 6, you learned how Copilot CLI works as an autonomous agent — planning, editing, running, and verifying in a loop. That works great for **single-focus tasks**: one function, one bug fix, one file.

But what about building a **real project** with multiple features that come together as one app? That's where **fleet mode** comes in.

### What Is Fleet Mode?

The `/fleet` command tells Copilot to **spin up multiple subagents** that work in parallel on different parts of your project. Think of it like this:

| Mode | Analogy | Best For |
|------|---------|----------|
| Regular agentic | One developer, one task at a time | Single files, bug fixes, utilities |
| **Fleet mode** | A team of developers working simultaneously | Multi-feature projects, full apps |

When you use `/fleet`, Copilot:
1. **Breaks your task** into independent subtasks
2. **Assigns each subtask** to a separate subagent
3. **Runs them in parallel** — all features built at once
4. **Coordinates the results** into a cohesive project

### When to Use Fleet Mode

```
┌─────────────────────────────────────────────────────┐
│              WHEN TO USE /FLEET                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ✅ USE /FLEET WHEN:                                │
│    • Project has 3+ files or features to build      │
│    • Work can be parallelized (independent pieces)  │
│    • You want a full app scaffold quickly           │
│    • Building something with multiple sections      │
│                                                     │
│  ❌ STICK WITH REGULAR AGENTIC WHEN:                │
│    • Single file or function                        │
│    • Sequential work (step B depends on step A)     │
│    • Quick bug fix or refactor                      │
│    • Exploring or prototyping ideas                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🔑 Designing for Parallelism: The Shared Pattern Approach

The secret to getting real parallelism from fleet mode is **how you structure the work**. If every task depends on the previous one, fleet can't parallelize — it's just sequential work with extra overhead.

### The Problem: Sequential Chains

```
❌ SEQUENTIAL (no parallelism)

  layout ──→ feature 1 ──→ feature 2 ──→ feature 3 ──→ assembly
  (each step waits for the previous one)
```

### The Solution: Shared Pattern Design

Instead, define a **shared structure** upfront (the "pattern"), then let subagents build each feature independently:

```
✅ SHARED PATTERN (maximum parallelism)

                  ┌──── Subagent A: Account Overview ───┐
                  │                                      │
  Shared    ──────┼──── Subagent B: Transactions ────────┼──── Assembly
  Pattern         │                                      │     (one app)
                  ├──── Subagent C: Transfers ───────────┤
                  │                                      │
                  └──── Subagent D: Loan Calculator ─────┘

  (Phase 1: quick)      (Phase 2: ALL in parallel!)       (Phase 3: combine)
```

### What Makes This Work?

The shared pattern gives every subagent the same building rules:

1. **Same HTML structure** — each feature is a `<section>` with a consistent layout
2. **Same CSS naming** — shared class conventions (e.g., `.feature-card`, `.feature-header`)
3. **Same visual style** — colors, fonts, spacing all defined once

With a shared pattern, each subagent knows exactly how to build its piece so they all fit together. This is exactly how real development teams work — agree on the pattern, then build independently.

---

## 🏗️ Fleet Mode in Practice

Let's walk through what happens when you use `/fleet` to build a bank app with 4 independent features.

**Your prompt:**
```
/fleet Plan and develop 4 simple independent features for a bank app.
Use the same pattern for all features so it's easy to connect them after.
Assemble all completed features into one simple app.
Use only html and css and open the website in a browser when finished.
```

**What Copilot does with /fleet:**

```
📋 Phase 1: Plan (quick, sequential)
🤖 Planning Agent:
   → Define shared pattern (HTML structure, CSS conventions)
   → Set up directory structure

📋 Phase 2: Build (ALL subagents run in parallel! ⚡)
🤖 Subagent A: Account Overview
   → Balance display, account details card

🤖 Subagent B: Transaction History
   → Transaction list, dates, amounts, categories

🤖 Subagent C: Transfer Money
   → Transfer form with recipient, amount, confirmation

🤖 Subagent D: Loan Calculator
   → Input fields for amount/rate/term, calculated results

📋 Phase 3: Assembly (sequential — combines everything)
🤖 Assembly Agent:
   → Combine all features into index.html
   → Merge styles into one stylesheet
   → Open in browser

⏱️ Phase 2 runs 4 agents simultaneously — this is where fleet shines!
```

### Why This Is Faster Than Sequential

```
Sequential:  Plan(30s) + Feature1(1m) + Feature2(1m) + Feature3(1m) + Feature4(1m) + Assembly(30s)
             = ~5 minutes total

Fleet:       Plan(30s) + max(Feature1, Feature2, Feature3, Feature4)(1m) + Assembly(30s)
             = ~2 minutes total  ← over 2x faster!
```

### Reviewing Fleet Output

After `/fleet` completes:

1. **Check the browser** — the app should open automatically
2. **Run `/diff`** to see all file changes
3. **Request adjustments** if anything needs tweaking

```
> /diff                    # Review all file changes
> "Make the header blue"   # Request adjustments conversationally
```

---

## 💡 Prompting Tips for Fleet Mode

### 1. Describe the Full Picture

Fleet needs to understand the complete project to divide work effectively:

❌ **Too narrow:** "Create an HTML section for account balances"
*(This is a single-agent task — no need for fleet)*

✅ **Full picture:** "Build a bank app with 4 features: account overview, transactions, transfers, and loan calculator"

### 2. Specify a Shared Pattern

Tell fleet to use the same structure so features fit together:

✅ "Use the same pattern for all features so it's easy to connect them after"

### 3. Say What Can Be Parallel

Explicitly mention which parts are independent:

✅ "Plan and develop 4 simple independent features"

### 4. Trust the Division of Labor

Don't micromanage which subagent does what — fleet handles task splitting automatically. Focus on **what** you want, not **how** to divide it.

---

## ✏️ Exercise: Build a Bank App with Fleet

Now it's your turn! Use `/fleet` to build a multi-feature app with maximum parallelism.

### Steps

1. **Enable experimental features** — run `/experimental` in Copilot CLI to activate fleet mode (it's currently an experimental feature)

2. **Paste this prompt:**

   ```
   /fleet Plan and develop 4 simple independent features for a bank app. Use the same pattern for all features so it's easy to connect them after. Assemble all completed features into one simple app. Use only html and css and open the website in a browser when finished.
   ```

3. **Watch the subagents work** — you should see multiple agents active simultaneously building different features

4. **Check the browser** — the assembled app should open automatically

5. **Review with `/diff`** — check the full set of changes across all files

### What Success Looks Like

After fleet completes, you should have something like:

```
bank-app/
├── index.html          # Assembled app with all 4 features
└── styles.css          # Shared styles for the whole app
```

With:
- ✅ 4 distinct feature sections visible in the browser
- ✅ Consistent styling across all features
- ✅ A clean, assembled single-page app
- ✅ Multiple subagents ran in parallel during the build

### Bonus Challenges

- 🌟 Ask Copilot to add a 5th feature (e.g., "Budget Tracker")
- 🌟 Ask Copilot to improve the visual design

---

## ✅ Verification

You've completed this lesson when:

- [ ] You used `/fleet` to build a multi-feature project
- [ ] The app opened in a browser with all features visible
- [ ] You reviewed the output with `/diff`

When you're ready, say **`verify`** to check your work.

---

## 📋 Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│        FLEET AGENTS CHEAT SHEET                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  FLEET MODE:                                        │
│    /fleet [prompt]    Delegate to parallel subagents │
│    Best for:          Multi-feature projects, apps   │
│    Avoid for:         Single files, quick fixes      │
│                                                     │
│  SHARED PATTERN DESIGN:                             │
│    1. Define a shared structure (HTML/CSS pattern)   │
│    2. Let subagents build features independently     │
│    3. Assemble into one cohesive app                │
│                                                     │
│  FLEET PROMPTING:                                   │
│    ✅ Describe the full project scope                │
│    ✅ Specify a shared pattern for consistency       │
│    ✅ Say what can be built in parallel              │
│    ❌ Don't create sequential dependency chains      │
│    ❌ Don't use fleet for single-file tasks          │
│                                                     │
│  PARALLELISM PATTERN:                               │
│    Plan ──→ [A, B, C, D in parallel] ──→ Assemble   │
│    (pattern)   (independent features)    (one app)   │
│                                                     │
│  AFTER FLEET:                                       │
│    /diff              Review all file changes        │
│    Check browser      See the assembled app          │
│    "Fix X"            Ask for adjustments            │
│                                                     │
│  COMPLEXITY GUIDE:                                  │
│    1 file ........... Regular agentic mode           │
│    2-3 files ........ Regular agentic (plan mode)    │
│    4+ files ......... Fleet mode (/fleet)            │
│    Full app ......... Fleet mode + shared pattern    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🎉 Summary

You've leveled up from single-agent tasks to coordinating a fleet of subagents!

| Concept | What You Learned |
|---------|-----------------|
| **Fleet Mode** | `/fleet` delegates to parallel subagents for multi-feature projects |
| **Shared Pattern** | Define a common structure so subagents can build independently |
| **Parallelism** | Structure work as Plan → [parallel builds] → Assemble |
| **Fleet Prompting** | Describe full scope, specify shared pattern, say what's parallel |
| **Reviewing Fleet Output** | `/diff` for changes, check the browser for the result |

### Key Takeaways

- 🚀 **Fleet = parallel power.** Multiple subagents build different features simultaneously
- 📝 **Shared patterns unlock parallelism.** Same structure means independent work that fits together
- ⏱️ **Minutes, not hours.** A multi-feature app built and assembled in ~2 minutes
- 🎯 **Describe what's parallel.** Tell fleet which pieces are independent to get real concurrency
- 🔍 **Always review.** `/diff` and visual inspection after fleet completes

---

## 📚 Additional Resources

- [GitHub Copilot CLI Documentation](https://docs.github.com/en/copilot/github-copilot-in-the-cli)
- [Copilot CLI Agentic Mode Guide](https://docs.github.com/en/copilot/using-github-copilot/using-copilot-coding-agent)

---

## 🚀 What's Next?

Continue to [Lesson 8: Instructions & Skills](./08-instructions.md) to learn how to personalize Copilot's behavior with custom instructions and skills.

---

*You've gone from directing a single agent to conducting an entire fleet. Shared patterns give them the blueprint, parallelism gives them the speed, and you stay in control of the vision. Now go build something ambitious! 🚀*

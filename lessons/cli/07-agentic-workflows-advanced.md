# Lesson 7: Advanced Agentic Workflows — Fleet Mode & TDD

**XP: 75** | **Difficulty: Intermediate-Advanced** | **Time: 30 minutes**

---

## 🎯 Learning Objectives

By the end of this lesson, you will:
- Understand when a task needs fleet mode vs. regular agentic mode
- Use `/fleet` to delegate work to parallel subagents
- Design tasks for maximum parallelism using a "contract-first" approach
- Apply TDD (Test-Driven Development) in agentic workflows
- Build a medium-complexity, multi-file project in minutes

---

## 🚀 From Single Agent to Fleet

In Lesson 6, you learned how Copilot CLI works as an autonomous agent — planning, editing, running, and verifying in a loop. That works great for **single-focus tasks**: one function, one bug fix, one file.

But what about building a **real project** with multiple files, components, styles, and tests? That's where **fleet mode** comes in.

### What Is Fleet Mode?

The `/fleet` command tells Copilot to **spin up multiple subagents** that work in parallel on different parts of your project. Think of it like this:

| Mode | Analogy | Best For |
|------|---------|----------|
| Regular agentic | One developer, one task at a time | Single files, bug fixes, utilities |
| **Fleet mode** | A team of developers working simultaneously | Multi-file projects, full features, apps |

When you use `/fleet`, Copilot:
1. **Breaks your task** into independent subtasks
2. **Assigns each subtask** to a separate subagent
3. **Runs them in parallel** — components, tests, styles all at once
4. **Coordinates the results** into a cohesive project

### When to Use Fleet Mode

```
┌─────────────────────────────────────────────────────┐
│              WHEN TO USE /FLEET                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ✅ USE /FLEET WHEN:                                │
│    • Project has 3+ files to create/edit            │
│    • Work can be parallelized (components, tests)   │
│    • You want a full app scaffold quickly           │
│    • Building something with frontend + logic       │
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

## 🧪 TDD with Agentic Workflows

Fleet mode pairs perfectly with **Test-Driven Development**. Instead of writing code first and testing later, you describe your tests upfront — and let the agents implement both.

### The Agentic TDD Flow

```
┌──────────────────────────────────────────────────────┐
│              AGENTIC TDD FLOW                        │
│                                                      │
│   ┌────────────────┐                                 │
│   │ DESCRIBE TESTS │  Tell Copilot what should pass  │
│   └───────┬────────┘                                 │
│           ↓                                          │
│   ┌────────────────┐                                 │
│   │   PLAN (ask)   │  Copilot asks clarifications    │
│   └───────┬────────┘                                 │
│           ↓                                          │
│   ┌────────────────┐                                 │
│   │  /FLEET BUILD  │  Subagents write tests + code   │
│   └───────┬────────┘  in parallel                    │
│           ↓                                          │
│   ┌────────────────┐                                 │
│   │   RUN TESTS    │  Verify everything passes       │
│   └───────┬────────┘                                 │
│           │ Failures?                                │
│           ↓                                          │
│   ┌────────────────┐     ┌──────────┐                │
│   │    ITERATE     │────→│   DONE   │                │
│   └────────────────┘     └──────────┘                │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Why TDD + Fleet Works So Well

1. **Tests define the contract** — subagents know exactly what the code must do
2. **Parallel safety** — tests and implementation can be written simultaneously because the tests define the interface
3. **Instant verification** — run the test suite immediately after fleet completes
4. **Catch integration issues early** — if subagents produce incompatible code, tests reveal it

### TDD Prompt Pattern

Here's the pattern that works well for agentic TDD:

```
"Build [project]. Here's what the tests should verify:
- [test case 1]
- [test case 2]
- [test case 3]
Write the tests first, then implement the code to pass them.
Use [framework] for testing. Run the tests to confirm they pass."
```

**Pro Tip:** You don't need to write perfect test specifications. Describing the *behaviors* you expect is enough — Copilot will translate them into proper test cases.

---

## 🔑 Designing for Parallelism: The Contract-First Approach

The secret to getting real parallelism from fleet mode is **how you structure the work**. If every task depends on the previous one, fleet can't parallelize — it's just sequential work with extra overhead.

### The Problem: Sequential Chains

A naive approach creates a dependency chain where nothing can run in parallel:

```
❌ SEQUENTIAL (no parallelism)

  utils ──→ hook ──→ components ──→ styles ──→ app
  (each step waits for the previous one)
```

### The Solution: Contract-First Design

Instead, define **shared interfaces** upfront (the "contract"), then let subagents build everything else independently:

```
✅ CONTRACT-FIRST (maximum parallelism)

                  ┌──── Subagent A: Utils + Tests ────┐
                  │                                    │
  Setup + ────────┼──── Subagent B: Components + Tests ┼──── Integration
  Contracts       │                                    │     + Final Tests
                  ├──── Subagent C: Styles (all CSS)  ─┤
                  │                                    │
                  └──── Subagent D: Hook + Tests ──────┘

  (Phase 1: quick)      (Phase 2: ALL in parallel!)     (Phase 3: wire up)
```

### What Makes This Work?

The contract phase creates a thin shared layer that all subagents can code against:

1. **Type definitions** — what does a Product look like? `{ id, name, quantity, price }`
2. **Function signatures** — what functions exist and what do they return?
3. **Component props** — what props does each component accept?

With these contracts in place, each subagent knows the shape of the inputs and outputs it needs to produce, even if the other pieces don't exist yet. This is exactly how real development teams work — agree on the API, then build independently.

### How to Prompt for Parallelism

Include the contract in your prompt so fleet can parallelize effectively:

```
Build a SaaS-style React inventory app. Here's the shared contract:

Product shape: { id: string, name: string, quantity: number, price: number }
Stock status: "in-stock" (qty >= 5), "low" (1-4), "out-of-stock" (0)
Stats shape: { totalProducts, totalValue, lowStockCount }

Build these in parallel:
1. Utils (inventory.js) — pure functions for add/getStats/getStockStatus
2. Layout (Sidebar, TopBar) — SaaS shell with nav, search, user avatar
3. Components (ProductList, AddProductForm, StatsBar) — rich SaaS-style UI
4. Styles (CSS modules) — dark sidebar, white cards, professional SaaS theme
5. Hook (useInventory) — state management using the util functions

Then wire everything together in App.jsx. Use TDD with Vitest.
```

By spelling out the data shapes, fleet subagents can all work at the same time without waiting for each other.

---

## 🏗️ Fleet Mode in Practice

Let's walk through what happens when you use `/fleet` to build a real project with the contract-first approach.

### Example: Building a SaaS-Style Inventory App

**Your prompt:**
```
/fleet Build a SaaS-style React inventory management app called "StockFlow Pro" using Vite.

Shared contract:
- Product: { id: string, name: string, quantity: number, price: number }
- Stock status: "in-stock" (qty >= 5), "low" (1-4), "out-of-stock" (0)
- Stats: { totalProducts: number, totalValue: number, lowStockCount: number }

WORKING features:
- Add new products via a form with validation (name, quantity, price required)
- Inline quantity editing (+ / - buttons to adjust stock)

SaaS UI chrome (visible but non-functional):
- Dark sidebar with nav items (Dashboard, Products, Categories, Suppliers, etc.)
- Top bar with search, notifications, user avatar
- Product table with toolbar (filter, bulk actions), checkboxes, SKU, pagination
- Stat cards with trend indicators
- Export/Import buttons

Build utils, layout shell, components, styles, and hook in parallel. Use TDD.
```

**What Copilot does with /fleet:**

```
📋 Phase 1: Setup (quick, sequential — must happen first)
🤖 Setup Agent:
   → Scaffold Vite + React + Vitest
   → Create shared types/contracts file
   → Set up directory structure

📋 Phase 2: Build (ALL subagents run in parallel! ⚡)
🤖 Subagent A: Utils + Unit Tests
   → Write tests for addProduct, getStats, getStockStatus, updateQuantity
   → Implement pure functions to pass tests

🤖 Subagent B: SaaS Layout Shell
   → Build Sidebar (nav items, logo, usage meter)
   → Build TopBar (search, notifications, user avatar)
   → All non-functional — pure UI chrome

🤖 Subagent C: Components + Component Tests
   → Write tests for ProductList, AddProductForm, StatsBar
   → Rich SaaS table with toolbar, checkboxes, SKU, pagination
   → Components are "dumb" — they receive data via props

🤖 Subagent D: All Styles
   → Create CSS modules for every component (7+ files)
   → Dark sidebar, white cards, blue primary, professional SaaS look
   → Can work entirely independently — no logic dependencies

🤖 Subagent E: Hook + Hook Tests
   → Write tests for useInventory (add, updateQuantity, computed stats)
   → Implement hook using util functions

📋 Phase 3: Integration (sequential — combines everything)
🤖 Integration Agent:
   → Wire App.jsx with sidebar + topbar + content layout
   → Run full test suite
   → Verify build succeeds

⏱️ Phase 2 runs 5 agents simultaneously — this is where fleet shines!
```

### Why This Is Faster Than Sequential

Without parallelism, each step waits for the last — total time is the **sum of all steps**:

```
Sequential:  Setup(1m) + Utils(2m) + Layout(2m) + Hook(2m) + Components(3m) + Styles(2m) + Integration(1m)
             = 13 minutes total

Fleet:       Setup(1m) + max(Utils, Layout, Hook, Components, Styles)(3m) + Integration(1m)
             = 5 minutes total  ← over 2x faster!
```

### Reviewing Fleet Output

After `/fleet` completes, you'll want to:

1. **Run `/diff`** to see all changes across all files
2. **Run the test suite** to verify everything passes
3. **Start the dev server** to visually inspect the app
4. **Request adjustments** if anything needs fixing

```
> /diff                    # Review all file changes
> npm test                 # Run the test suite
> npm run dev              # Start the dev server to see the app
> "Make the header blue"   # Request adjustments conversationally
```

---

## 💡 Prompting for Fleet Mode

Fleet prompts are different from single-agent prompts. You're describing an **entire project**, not a single task.

### 1. Define the Contract First

Give fleet the shared data shapes so subagents can work independently:

✅ "Product: { id, name, quantity, price }. Stats: { totalProducts, totalValue, lowStockCount }."

### 2. Describe the Full Picture

Fleet needs to understand the complete project to divide work effectively:

❌ **Too narrow:** "Create a React component for a product list"
*(This is a single-agent task — no need for fleet)*

✅ **Full picture:** "Build a React inventory app with a product list, add form, quantity editing, summary stats, styling, and tests"

### 3. Mention the Tech Stack

Fleet subagents need to agree on tools:

✅ "Use Vite for scaffolding, Vitest for testing, CSS modules for styling"

### 4. Tell Fleet What Can Be Parallel

Explicitly mention which parts are independent:

✅ "Build utils, components, styles, and hook in parallel"

### 5. Specify Test Strategy

Tell fleet to use TDD so tests come first:

✅ "Write tests first using TDD, then implement code to pass them"

### 6. Trust the Division of Labor

Don't micromanage which subagent does what — fleet handles task splitting automatically. Focus on **what** you want, not **how** to divide it.

---

## ✏️ Exercise: Build a React Inventory App with Fleet

Now it's your turn! Use `/fleet` with TDD and the contract-first approach to build an app with maximum parallelism.

### Your Task

Build a **SaaS-style inventory management app** using fleet mode and TDD. The app should look like a real $50/mo SaaS product — complete with sidebar navigation, top bar, and rich UI chrome — but only two features actually work.

### Scope: Look Like a SaaS, Build Like a Tutorial

Only two features are **functional** — but the full SaaS UI should be visible:

**Working features:**
1. **Add products** — a form with name, quantity, price fields and validation
2. **Adjust quantity** — +/- buttons on each product row to update stock levels

**SaaS UI chrome (visible but non-functional):**
- Sidebar with navigation: Dashboard, Products (active), Categories, Suppliers, Orders, Reports, Settings
- Top bar with search, notifications, and user avatar
- Product table with toolbar (search/filter, bulk actions), checkboxes, SKU column, category column, actions menu, pagination
- Export/Import buttons on the page header
- Stat cards with trend indicators

### Steps

1. **Enable experimental features** — run `/experimental` in Copilot CLI to activate fleet mode (it's currently an experimental feature)

2. **Enter plan mode** — press **Shift+Tab** or use `/plan`

3. **Paste this prompt** (or customize it):

   ```
   Build a professional SaaS-style React inventory management app using Vite.
   It should look like a real inventory SaaS product called "StockFlow Pro".

   Shared contract:
   - Product: { id: string, name: string, quantity: number, price: number }
   - Stock status: "in-stock" (qty >= 5), "low" (1-4), "out-of-stock" (0)
   - Stats: { totalProducts, totalValue, lowStockCount }

   WORKING features (these must actually function):
   - Add products via form with validation (name, quantity, price required)
   - Quantity adjustment (+ / - buttons per product row)

   SaaS UI shell (visible but non-functional — makes it look like a real product):
   - Dark sidebar (slate-900) with nav: Dashboard, Products (active), Categories,
     Suppliers, Orders (with "3" notification badge), Reports, Settings.
     Logo "StockFlow" with "Pro" badge. Footer with usage bar "680/1,000 products".
   - Top bar with search input (read-only, shows ⌘K shortcut), notification bell
     with red dot, help button, user avatar with initials + name + "Admin" role.
   - Product table toolbar: search/filter input, "All Status" dropdown,
     "Category" dropdown, "Bulk Actions" dropdown (all non-functional).
   - Table columns: checkbox, product thumbnail (colored circle with initial),
     name, SKU (auto-generated from product ID), category ("General"), quantity
     with +/- buttons, price, status badge, actions menu ("⋯").
   - Pagination footer: "Showing 1-X of X products" + page buttons.
   - Page header with Export and Import buttons (non-functional).
   - 4 stat cards: Total Products, Total Value, In Stock, Low Stock — each with
     emoji icon and decorative trend text.

   Color scheme: dark sidebar (#0f172a), light content (#f1f5f9), white cards,
   blue primary (#3b82f6), slate text, green/amber/red status badges.

   Build these in parallel:
   1. Utils (inventory.js) — addProduct, getStats, getStockStatus, updateQuantity
   2. Layout (Sidebar, TopBar) — SaaS shell, non-functional chrome
   3. Components (ProductList, AddProductForm, StatsBar) — rich SaaS-style UI
   4. Styles — CSS modules for all components, professional SaaS theme
   5. Hook (useInventory) — state management wrapping utils

   Then wire together in App.jsx with sidebar + topbar + content layout.
   Use TDD with Vitest + React Testing Library for the functional parts.
   ```

4. **Answer clarifying questions** — Copilot may ask about:
   - Low stock threshold (suggest: quantity < 5)
   - Data persistence (suggest: in-memory only)
   - Color scheme details

5. **Review the plan** — press **Ctrl+Y** to see how Copilot divides the work

6. **Look for parallelism!** — the plan should show multiple subagents running at the same time in Phase 2. If everything is sequential, refine your prompt to emphasize what can be parallel.

7. **Approve and switch to fleet** — say **"Use /fleet to implement this"**

8. **Watch the subagents work** — you should see multiple agents active simultaneously

9. **Run the test suite** — `npm test` to verify all tests pass

10. **Start the dev server** — `npm run dev` to see the working app

11. **Try it out** — add a product, click +/- to adjust quantities, watch stats update

12. **Review with `/diff`** — check the full set of changes

### What Success Looks Like

After fleet completes, you should have:

```
inventory-app/
├── src/
│   ├── App.jsx                    # SaaS layout — sidebar + topbar + content
│   ├── App.module.css             # Layout with sidebar offset
│   ├── index.css                  # Global reset + SaaS base styles
│   ├── components/
│   │   ├── Sidebar.jsx            # Dark nav sidebar (non-functional)
│   │   ├── Sidebar.module.css
│   │   ├── TopBar.jsx             # Search, notifications, user (non-functional)
│   │   ├── TopBar.module.css
│   │   ├── ProductList.jsx        # Rich table with toolbar + pagination
│   │   ├── ProductList.module.css
│   │   ├── ProductList.test.jsx
│   │   ├── AddProductForm.jsx     # Add product form with validation
│   │   ├── AddProductForm.module.css
│   │   ├── AddProductForm.test.jsx
│   │   ├── StatsBar.jsx           # 4 stat cards with trends
│   │   ├── StatsBar.module.css
│   │   └── StatsBar.test.jsx
│   ├── hooks/
│   │   ├── useInventory.js        # State management (add, updateQty)
│   │   └── useInventory.test.jsx
│   └── utils/
│       ├── inventory.js           # Pure business logic
│       └── inventory.test.js
├── package.json
├── vite.config.js
└── vitest.config.js
```

With:
- ✅ All tests passing
- ✅ A SaaS-looking app with dark sidebar, top bar, and rich product table
- ✅ Two working features: add products and adjust quantities
- ✅ Full SaaS chrome: nav, search, filters, pagination, export/import, user menu
- ✅ Stats updating in real time with decorative trend indicators
- ✅ Professional blue/slate styling that looks like a real product
- ✅ Multiple subagents ran in parallel during the build

### Bonus Challenges

- 🌟 Make the search/filter bar in the product table actually work
- 🌟 Add sorting when clicking column headers
- 🌟 Make the sidebar navigation switch between placeholder pages
- 🌟 Add localStorage persistence (and a test for it)
- 🌟 Try the same project **without** fleet — compare the time and experience
- 🌟 Add a "delete product" button in the actions menu with a confirmation dialog

---

## ✅ Verification

You've completed this lesson when:

- [ ] You used `/fleet` to build a multi-file project
- [ ] Your project was built with TDD (tests written before/alongside implementation)
- [ ] The test suite passes
- [ ] The app runs and looks like a real SaaS product (sidebar, top bar, rich table)
- [ ] Add product and quantity +/- buttons actually work
- [ ] You reviewed the output with `/diff`

When you're ready, say **`verify`** to check your work.

---

## 📋 Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│        ADVANCED AGENTIC WORKFLOWS CHEAT SHEET       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  FLEET MODE:                                        │
│    /fleet [prompt]    Delegate to parallel subagents │
│    Best for:          Multi-file projects, full apps │
│    Avoid for:         Single files, quick fixes      │
│                                                     │
│  CONTRACT-FIRST DESIGN:                             │
│    1. Define shared data shapes (Product, Stats)     │
│    2. Define function signatures + component props   │
│    3. Let subagents build independently in parallel  │
│    4. Wire together in a final integration step      │
│                                                     │
│  AGENTIC TDD:                                       │
│    1. Describe behaviors/tests you expect            │
│    2. Let Copilot write tests first                  │
│    3. Then implement code to pass them               │
│    4. Run test suite to verify                       │
│    5. Iterate on failures                            │
│                                                     │
│  FLEET PROMPTING:                                   │
│    ✅ Define the contract (data shapes, interfaces)  │
│    ✅ Describe the full project scope                │
│    ✅ Specify tech stack (Vite, Vitest, etc.)        │
│    ✅ Say "build X, Y, Z in parallel"               │
│    ✅ Say "TDD — write tests first"                  │
│    ❌ Don't create sequential dependency chains      │
│    ❌ Don't use fleet for single-file tasks          │
│                                                     │
│  PARALLELISM PATTERN:                               │
│    Setup ──→ [A, B, C, D in parallel] ──→ Integrate │
│    (contracts)  (independent work)       (wire up)   │
│                                                     │
│  AFTER FLEET:                                       │
│    /diff              Review all file changes        │
│    npm test           Run the test suite             │
│    npm run dev        Start the dev server           │
│    "Fix X"            Ask for adjustments            │
│                                                     │
│  COMPLEXITY GUIDE:                                  │
│    1 file ........... Regular agentic mode           │
│    2-3 files ........ Regular agentic (plan mode)    │
│    4+ files ......... Fleet mode (/fleet)            │
│    Full app ......... Fleet mode + TDD + contracts   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🎉 Summary

You've leveled up from single-agent tasks to coordinating a fleet of subagents!

| Concept | What You Learned |
|---------|-----------------|
| **Fleet Mode** | `/fleet` delegates to parallel subagents for multi-file projects |
| **Contract-First** | Define shared data shapes upfront so subagents can work independently |
| **Parallelism** | Structure work as Setup → [parallel builds] → Integration |
| **Agentic TDD** | Describe tests first → agents write tests + code → verify → iterate |
| **Fleet Prompting** | Define contracts, describe full scope, specify what's parallel |
| **Reviewing Fleet Output** | `/diff` for changes, `npm test` for tests, `npm run dev` for visual check |

### Key Takeaways

- 🚀 **Fleet = parallel power.** Multiple subagents build different parts of your project simultaneously
- 📝 **Contracts unlock parallelism.** Define shared interfaces first, then everything can be built independently
- 🧪 **TDD + fleet = confidence.** Tests define the contract, fleet implements to pass them
- ⏱️ **Minutes, not hours.** A professional multi-file app in ~5 minutes
- 🎯 **Describe what's parallel.** Tell fleet which pieces are independent to get real concurrency
- 🔍 **Always review.** `/diff`, test suite, and visual inspection after fleet completes

---

## 📚 Additional Resources

- [GitHub Copilot CLI Documentation](https://docs.github.com/en/copilot/github-copilot-in-the-cli)
- [Copilot CLI Agentic Mode Guide](https://docs.github.com/en/copilot/using-github-copilot/using-copilot-coding-agent)
- [Test-Driven Development with AI](https://docs.github.com/en/copilot/using-github-copilot/prompt-engineering-for-github-copilot)

---

## 🚀 What's Next?

Continue to [Lesson 8: Instructions & Skills](./08-instructions.md) to learn how to personalize Copilot's behavior with custom instructions and skills.

---

*You've gone from directing a single agent to conducting an entire fleet. Contracts give them the blueprint, parallelism gives them the speed, and you stay in control of the vision. Now go build something ambitious! 🚀*

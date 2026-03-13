# Plan: WealthPulse — React Wealth Management Dashboard

## Problem

Build a SaaS-style React wealth management dashboard called "WealthPulse" for the Lesson 7 exercise. The app needs two working features (add assets, inline price editing) wrapped in a polished fintech UI with dark sidebar, top bar, stat cards, and styled asset table. Located at `exercises/cli/wealth-pulse/`.

## Approach

Use Vite + React + Vitest. Define shared contracts (Asset, Performance, Stats types) upfront, then build four parallel workstreams: utils, layout, components, and hook. Wire everything together in App.jsx. In-memory state only, with 3-4 sample assets pre-loaded. No TDD — tests written alongside or after implementation.

## Workplan

### Phase 1: Scaffold + Contracts (sequential — foundation)

- [x] **1.** Scaffold Vite + React project at `exercises/cli/wealth-pulse/`
  - `npm create vite@latest` with React template
  - Install dependencies: `vitest`, `@testing-library/react`, `@testing-library/jest-dom`, `jsdom`
  - Configure `vite.config.js` and `vitest.config.js`
  - Set up directory structure: `src/components/`, `src/hooks/`, `src/utils/`

- [x] **2.** Create shared contracts file (`src/utils/contracts.js`)
  - Asset shape: `{ id: string, name: string, ticker: string, type: "stock"|"bond"|"etf", shares: number, avgCost: number, currentPrice: number }`
  - Performance enum: `"gain"` (current > avg), `"loss"` (current < avg), `"flat"` (equal)
  - Stats shape: `{ totalValue, totalGainLoss, totalGainLossPercent, assetCount }`
  - Sample assets: 3-4 demo assets (e.g., AAPL stock, VBTLX bond, VOO ETF, MSFT stock)
  - Factory function: `createAsset(overrides)` for easy asset creation

### Phase 2: Parallel Build (4 independent workstreams ⚡)

- [x] **3.** Utils (`src/utils/portfolio.js`) + tests
  - `getPerformance(asset)` → returns "gain" | "loss" | "flat"
  - `calculateGainLoss(asset)` → returns `{ amount, percent }`
  - `calculateStats(assets)` → returns Stats shape
  - `getBestPerformer(assets)` → returns asset with highest gain %
  - `formatCurrency(value)` → format as $X,XXX.XX
  - `formatPercent(value)` → format as +X.XX% / -X.XX%
  - Write `portfolio.test.js` covering all functions

- [x] **4.** Layout: Sidebar + TopBar + styles
  - `Sidebar.jsx` + `Sidebar.module.css` — dark bg (#0f172a), logo "WealthPulse", nav items: Overview, Portfolio (active state), Watchlist, Reports, Settings. Icons optional (emoji or text). Non-functional links.
  - `TopBar.jsx` + `TopBar.module.css` — search input placeholder, notification bell icon, user avatar circle "JD". Non-functional.
  - `index.css` — global reset, CSS variables for color tokens: `--sidebar-bg: #0f172a`, `--content-bg: #f1f5f9`, `--accent: #10b981`, `--gain: #22c55e`, `--loss: #ef4444`

- [x] **5.** Components: AssetTable, AddAssetForm, StatsBar + styles
  - `StatsBar.jsx` + `StatsBar.module.css` — 4 stat cards (Total Value, Day's Change, Best Performer, # Assets) with trend arrows (▲/▼). Receives `stats` and `bestPerformer` as props.
  - `AddAssetForm.jsx` + `AddAssetForm.module.css` — form with: name, ticker, type (dropdown: stock/bond/etf), shares, avg cost, current price. Calls `onAdd(asset)` prop. Default type: "stock". Clear form on submit.
  - `AssetTable.jsx` + `AssetTable.module.css` — table rows with: name+ticker, type badge (colored by type), shares, avg cost, current price (editable on pencil click), gain/loss %, performance badge (green/red). Pencil icon toggles edit mode per row → input + save button. Calls `onUpdatePrice(id, newPrice)` prop.
  - Write tests: `StatsBar.test.jsx`, `AddAssetForm.test.jsx`, `AssetTable.test.jsx`

- [x] **6.** Hook: `usePortfolio` + tests
  - `src/hooks/usePortfolio.js`
  - State: `assets` array, initialized with sample assets from contracts
  - `addAsset(assetData)` — generates id, adds to state
  - `updatePrice(id, newPrice)` — updates currentPrice for given asset
  - Computed: `stats` (via calculateStats), `bestPerformer` (via getBestPerformer)
  - Returns: `{ assets, stats, bestPerformer, addAsset, updatePrice }`
  - Write `usePortfolio.test.jsx` using `@testing-library/react` renderHook

### Phase 3: Integration (sequential — wire everything together)

- [x] **7.** Wire App.jsx + layout styles
  - `App.jsx` — SaaS layout: Sidebar (fixed left), TopBar (top), main content area with StatsBar + AddAssetForm + AssetTable
  - `App.module.css` — grid/flex layout: sidebar 240px fixed, content offset, responsive-ish
  - Connect usePortfolio hook to all components via props
  - Verify the app renders correctly

- [x] **8.** Final verification
  - Run `npm test` — all tests pass
  - Run `npm run dev` — app loads, looks like a SaaS product
  - Test add asset flow: fill form → submit → appears in table → stats update
  - Test inline edit: pencil → change price → save → gain/loss recalculates
  - Run `npm run build` — production build succeeds

## Notes

- **Location:** `exercises/cli/wealth-pulse/`
- **Data:** In-memory only, no localStorage. 3-4 sample assets pre-loaded.
- **Styling:** CSS Modules throughout. Dark sidebar (#0f172a), light content (#f1f5f9), emerald accent (#10b981), green (#22c55e) for gains, red (#ef4444) for losses.
- **Parallel tasks:** Items 3, 4, 5, 6 are fully independent and can be built simultaneously by fleet subagents.
- **Contracts file** is the shared dependency — must exist before parallel phase.
- **No TDD** — tests written alongside implementation, not before.

## Dependencies

```
Phase 1 (tasks 1-2) → Phase 2 (tasks 3-6, all parallel) → Phase 3 (tasks 7-8)
```

| Task | Depends On |
|------|-----------|
| 1. Scaffold | — |
| 2. Contracts | 1 |
| 3. Utils + tests | 2 |
| 4. Layout + styles | 2 |
| 5. Components + styles + tests | 2 |
| 6. Hook + tests | 2 |
| 7. Wire App.jsx | 3, 4, 5, 6 |
| 8. Final verification | 7 |

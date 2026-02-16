---
name: dashboard
description: "Generate a visual progress dashboard showing lesson completion, XP, achievements, and level. Invoke when user says 'dashboard', 'show progress', or 'my stats'."
---

## Purpose

This skill generates a rich, visual progress dashboard in markdown format. It reads `progress.json` from the repository root and renders a comprehensive view of the learner's journey including their profile, XP progression, lesson status, achievements, and stats.

## Instructions

### Step 1: Read Progress Data

Read `progress.json` from the repository root. The file follows this schema:

```json
{
  "version": "1.0",
  "started_at": "<ISO timestamp or null>",
  "skillLevel": "<beginner|intermediate|advanced|expert|null>",
  "currentLesson": <number or null>,
  "xp": <number>,
  "achievements": ["<badge_id>", ...],
  "skippedLessons": [<lesson numbers>],
  "lessons": {
    "<lesson_number>": {
      "completed_at": "<ISO timestamp>",
      "xp_earned": <number>,
      "exercises_completed": <number>,
      "exercises_total": <number>
    }
  }
}
```

If `progress.json` does not exist or contains invalid JSON, inform the user and suggest running the onboarding skill first.

### Step 2: Determine Level from XP

Calculate the learner's level using these thresholds:

| Level | XP Range  | Title        |
|-------|-----------|--------------|
| 1     | 0–99      | Novice       |
| 2     | 100–249   | Apprentice   |
| 3     | 250–399   | Practitioner |
| 4     | 400–474   | Expert       |
| 5     | 475       | Master       |

```
getLevel(xp):
  if xp >= 475: return { level: 5, title: "Master" }
  if xp >= 400: return { level: 4, title: "Expert" }
  if xp >= 250: return { level: 3, title: "Practitioner" }
  if xp >= 100: return { level: 2, title: "Apprentice" }
  return { level: 1, title: "Novice" }
```

### Step 3: Build the XP Progress Bar

Render a text-based XP bar showing progress toward maximum XP (475). Use filled blocks `█` and empty blocks `░` across 20 characters.

```
buildXpBar(xp, maxXp=475):
  filled = floor((xp / maxXp) * 20)
  empty = 20 - filled
  return "█" repeated filled times + "░" repeated empty times
```

Example: 250 XP → `█████████░░░░░░░░░░░` (9 filled, 11 empty)

### Step 4: Build Lesson Rows

For each of the 9 lessons, determine the status and render a row:

**Lesson Names:**

| # | Name | Section | XP |
|---|------|---------|-----|
| 1 | Introduction to Copilot Chat | Chat | 25 |
| 2 | Effective Prompting | Chat | 25 |
| 3 | Slash Commands | Chat | 25 |
| 4 | Chat Participants (@workspace, @terminal) | Chat | 25 |
| 5 | Copilot CLI Fundamentals | CLI | 50 |
| 6 | Agentic Workflows in CLI | CLI | 50 |
| 7 | Agentic Workflows Advanced | CLI | 75 |
| 8 | Instructions & Skills | Customization | 100 |
| 9 | Building an MCP Tool | Advanced | 100 |

**Status indicators:**

| Condition | Indicator | Display |
|-----------|-----------|---------|
| Lesson exists in `lessons` with `completed_at` | ✅ Completed | `✅` with XP earned |
| Lesson number equals `currentLesson` | → In Progress | `→` with "(current)" label |
| Lesson number is in `skippedLessons` | ⏭️ Skipped | `⏭️` with "(skipped)" label |
| Otherwise | ○ Not Started | `○` |

### Step 5: Build Achievements Section

Reference these achievement definitions:

| Badge ID | Name | Emoji | Criteria |
|----------|------|-------|----------|
| `first_lesson` | First Steps | 🎯 | Complete any lesson |
| `chat_master` | Chat Master | 💬 | Complete lessons 1–4 |
| `cli_pro` | CLI Pro | ⌨️ | Complete lessons 5–7 |
| `customizer` | Customizer | 🎨 | Complete lessons 8–9 |
| `mcp_explorer` | MCP Explorer | 🔌 | Complete lesson 9 |
| `completionist` | Completionist | 🏆 | Complete all lessons |
| `century` | Century Club | 💯 | Earn 100+ XP |
| `power_learner` | Power Learner | ⚡ | Earn 500+ XP |

For each achievement:
- If the badge ID is in the `achievements` array → show as **earned**: `emoji Name`
- If not earned → show as **locked**: `○ Name (locked)`

### Step 6: Calculate Stats

```
completedCount = count of entries in lessons object
skippedCount = length of skippedLessons array
totalLessons = 9
effectiveLessons = totalLessons - skippedCount
completionPercent = floor((completedCount / effectiveLessons) * 100)
totalPossibleXp = 475
```

### Step 7: Render the Dashboard

Combine all sections into this markdown format:

```markdown
# 📊 Progress Dashboard

## 👤 Learner Profile

| | |
|---|---|
| **Skill Level** | {skillLevel or "Not set"} |
| **Started** | {started_at formatted as YYYY-MM-DD, or "Not started"} |
| **Level** | Level {level} — {title} |

## 📈 Current Progress

**XP: {xp} / 475**

`[{xpBar}]` {completionPercent}%

**Current Lesson:** {currentLesson or "None"} — {lessonName}

## 📚 Lessons

| # | Lesson | Section | Status | XP |
|---|--------|---------|--------|----|
| 1 | Introduction to Copilot Chat | Chat | ✅ Completed | 25 |
| 2 | Effective Prompting | Chat | ✅ Completed | 25 |
| ... | ... | ... | ... | ... |

## 🏅 Achievements ({earnedCount}/{totalAchievements})

| Status | Badge | Name |
|--------|-------|------|
| 🎯 | First Steps | ✅ Earned |
| 💬 | Chat Master | ✅ Earned |
| ⌨️ | CLI Pro | ○ Locked |
| ... | ... | ... |

## 📊 Stats

| Metric | Value |
|--------|-------|
| **Total XP** | {xp} / 475 |
| **Lessons Completed** | {completedCount} / {effectiveLessons} |
| **Lessons Skipped** | {skippedCount} |
| **Completion** | {completionPercent}% |
| **Achievements Unlocked** | {earnedCount} / 8 |
```

## Example Output

Below is an example dashboard for a learner who has completed lessons 1–6, is currently on lesson 7, with skill level "beginner" and started on 2025-01-15:

**progress.json state:**
```json
{
  "version": "1.0",
  "started_at": "2025-01-15T10:00:00Z",
  "skillLevel": "beginner",
  "currentLesson": 7,
  "xp": 200,
  "achievements": ["first_lesson", "chat_master", "century"],
  "skippedLessons": [],
  "lessons": {
    "1": { "completed_at": "2025-01-15T11:00:00Z", "xp_earned": 25, "exercises_completed": 3, "exercises_total": 3 },
    "2": { "completed_at": "2025-01-16T10:00:00Z", "xp_earned": 25, "exercises_completed": 4, "exercises_total": 4 },
    "3": { "completed_at": "2025-01-17T10:00:00Z", "xp_earned": 25, "exercises_completed": 3, "exercises_total": 3 },
    "4": { "completed_at": "2025-01-18T10:00:00Z", "xp_earned": 25, "exercises_completed": 3, "exercises_total": 3 },
    "5": { "completed_at": "2025-01-19T10:00:00Z", "xp_earned": 50, "exercises_completed": 4, "exercises_total": 4 },
    "6": { "completed_at": "2025-01-20T10:00:00Z", "xp_earned": 50, "exercises_completed": 3, "exercises_total": 3 }
  }
}
```

**Rendered dashboard:**

---

# 📊 Progress Dashboard

## 👤 Learner Profile

| | |
|---|---|
| **Skill Level** | beginner |
| **Started** | 2025-01-15 |
| **Level** | Level 2 — Apprentice |

## 📈 Current Progress

**XP: 200 / 475**

`[████████░░░░░░░░░░░░]` 67%

**Current Lesson:** 7 — Agentic Workflows Advanced

## 📚 Lessons

| # | Lesson | Section | Status | XP |
|---|--------|---------|--------|----|
| 1 | Introduction to Copilot Chat | Chat | ✅ Completed | 25 |
| 2 | Effective Prompting | Chat | ✅ Completed | 25 |
| 3 | Slash Commands | Chat | ✅ Completed | 25 |
| 4 | Chat Participants (@workspace, @terminal) | Chat | ✅ Completed | 25 |
| 5 | Copilot CLI Fundamentals | CLI | ✅ Completed | 50 |
| 6 | Agentic Workflows in CLI | CLI | ✅ Completed | 50 |
| 7 | Agentic Workflows Advanced | CLI | → In Progress | — |
| 8 | Instructions & Skills | Customization | ○ Not Started | — |
| 9 | Building an MCP Tool | Advanced | ○ Not Started | — |

## 🏅 Achievements (3/8)

| Status | Badge | Name |
|--------|-------|------|
| 🎯 | First Steps | ✅ Earned |
| 💬 | Chat Master | ✅ Earned |
| ⌨️ | CLI Pro | ○ Locked |
| 🎨 | Customizer | ○ Locked |
| 🔌 | MCP Explorer | ○ Locked |
| 🏆 | Completionist | ○ Locked |
| 💯 | Century Club | ✅ Earned |
| ⚡ | Power Learner | ○ Locked |

## 📊 Stats

| Metric | Value |
|--------|-------|
| **Total XP** | 200 / 475 |
| **Lessons Completed** | 6 / 9 |
| **Lessons Skipped** | 0 |
| **Completion** | 67% |
| **Achievements Unlocked** | 3 / 8 |

---

## Edge Cases

- **No progress yet:** Show all lessons as `○ Not Started`, XP bar empty, all achievements locked. Display a message: "You haven't started yet! Run the onboarding to begin your journey."
- **All lessons complete:** Show all lessons as `✅ Completed`, XP bar full, congratulatory message.
- **Skipped lessons:** Skipped lessons show `⏭️ Skipped` and are excluded from the effective lesson count when calculating completion percentage.
- **`currentLesson` is null:** If `started_at` exists, default to lesson 1. If `started_at` is null, show "Not started".
- **XP exceeds 475:** Cap the progress bar at 20 filled blocks but still show the actual XP number.

## Integration

This skill is read-only — it does not modify `progress.json`. It only reads and renders. For updates, use the `progress` skill.

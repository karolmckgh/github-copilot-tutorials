---
name: progress
description: "Track and manage learner progress through the tutorial. Read/update XP, achievements, lesson completion status. Invoke when user asks about progress, XP, or achievements."
---

## Purpose

This skill provides a centralized way to read and update the learner's progress through the GitHub Copilot tutorials. It manages XP, achievements, lesson completion, and provides progress summaries.

## Schema Reference

The `progress.json` file uses this schema:

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

## XP Values

| Lesson Range | Difficulty | XP per Lesson |
|--------------|------------|---------------|
| Lessons 1-4  | Beginner   | 25 XP         |
| Lessons 5-7  | Intermediate | 50 XP       |
| Lessons 8-9  | Advanced   | 100 XP        |

### XP Calculation Function

```
getXpForLesson(lessonNumber):
  if lessonNumber <= 4: return 25
  if lessonNumber <= 7: return 50
  return 100
```

## Achievements

| Badge ID | Name | Criteria | Icon |
|----------|------|----------|------|
| `first_lesson` | First Steps | Complete your first lesson | 🎯 |
| `chat_master` | Chat Master | Complete all Chat lessons (1-4) | 💬 |
| `cli_pro` | CLI Pro | Complete all CLI lessons (5-7) | ⌨️ |
| `customizer` | Customizer | Complete lessons 8-9 | 🎨 |
| `mcp_explorer` | MCP Explorer | Complete lesson 9 | 🔌 |
| `completionist` | Completionist | Complete all lessons | 🏆 |
| `century` | Century Club | Earn 100+ XP | 💯 |
| `power_learner` | Power Learner | Earn 500+ XP | ⚡ |

## Operations

### Read Operations

#### Get Current Progress

Read `progress.json` and return the full state. Use this when displaying progress summary.

#### Get Current Lesson

```
Read progress.json
Return currentLesson value (or 1 if null and started_at exists)
```

#### Get XP Total

```
Read progress.json
Return xp value
```

#### Check Achievement

```
Read progress.json
Return true if achievements array contains the badge_id
```

#### Get Completed Lessons

```
Read progress.json
Return Object.keys(lessons).map(Number).sort()
```

### Update Operations

#### Mark Lesson Complete

When a lesson is completed:

```
1. Read progress.json
2. If started_at is null, set started_at = new Date().toISOString()
3. If lessons[lessonNumber] already exists AND has completed_at:
   → Skip XP award (don't duplicate), just respond "Already completed!"
4. Calculate xp_earned = getXpForLesson(lessonNumber)
5. Set lessons[lessonNumber] = {
     completed_at: new Date().toISOString(),
     xp_earned: xp_earned,
     exercises_completed: exercisesCompleted,
     exercises_total: exercisesTotal
   }
6. Add xp_earned to total xp
7. Set currentLesson = lessonNumber + 1 (if next lesson exists and not skipped)
8. Check and award any newly unlocked achievements
9. Write updated progress.json
```

#### Add XP (Bonus)

For bonus XP (not tied to lesson completion):

```
1. Read progress.json
2. Add amount to xp
3. Check for XP-based achievements (century, power_learner)
4. Write updated progress.json
```

#### Award Achievement

```
1. Read progress.json
2. If badge_id not in achievements:
   - Add badge_id to achievements array
   - Return { awarded: true, badge: badge_id }
3. Else return { awarded: false, reason: "already_earned" }
4. Write updated progress.json
```

#### Check and Award Achievements

Run after any progress update to check for newly unlocked achievements:

```
1. Read current progress
2. For each achievement, check criteria:
   - first_lesson: lessons object has at least 1 entry
   - chat_master: lessons has all of [1,2,3,4] OR all are in skippedLessons
   - cli_pro: lessons has all of [5,6,7] that are NOT in skippedLessons
   - customizer: lessons has all of [8,9]
   - mcp_explorer: lessons has 9
   - completionist: all lessons completed OR skipped (nothing remaining)
   - century: xp >= 100
   - power_learner: xp >= 500
3. Award any newly qualified achievements
```

## Progress Summary Format

When user asks to see their progress, display:

```
╔═══════════════════════════════════════════════════════╗
║              📊 YOUR LEARNING PROGRESS                ║
╠═══════════════════════════════════════════════════════╣
║  Level: <skillLevel>                                  ║
║  Current Lesson: <currentLesson>                      ║
║  Total XP: <xp> ✨                                    ║
╠═══════════════════════════════════════════════════════╣
║  LESSONS                                              ║
║  ──────────────────────────────────────────           ║
║  ✅ Lesson 1: Introduction to Copilot Chat (25 XP)   ║
║  ✅ Lesson 2: Effective Prompting (25 XP)            ║
║  ⏭️  Lesson 3: (skipped)                              ║
║  → Lesson 4: Chat Participants (@workspace, @terminal) (current) ║
║  ○ Lesson 5: Copilot CLI Fundamentals                ║
║  ...                                                  ║
╠═══════════════════════════════════════════════════════╣
║  ACHIEVEMENTS (<count>/<total>)                       ║
║  ──────────────────────────────────────────           ║
║  🎯 First Steps                                       ║
║  💬 Chat Master                                       ║
║  ○ CLI Pro (complete lessons 5-7)                    ║
║  ...                                                  ║
╠═══════════════════════════════════════════════════════╣
║  Progress: [████████░░░░░░░░] 40%                    ║
║  Next milestone: CLI Pro (3 lessons away)            ║
╚═══════════════════════════════════════════════════════╝
```

### Legend
- `✅` = Completed
- `⏭️` = Skipped (based on skill level)
- `→` = Current lesson
- `○` = Not started / Not earned

### Progress Percentage Formula
```
effective_lessons = total_lessons - skipped_lessons_count
completed_lessons = count of lessons with completed_at
progress_percent = (completed_lessons / effective_lessons) × 100
```
Example: 4 completed, 0 skipped, 9 total → 4/9 = 44%
Example: 2 completed, 4 skipped, 9 total → 2/5 = 40%

## Integration with Other Skills

### Onboarding Skill
After onboarding completes, it should call progress operations to:
1. Set `skillLevel`
2. Set `skippedLessons`
3. Set `currentLesson` based on starting point

### Lesson Skills
After a lesson is completed, call:
1. `Mark Lesson Complete` with lesson number and exercise counts
2. The operation automatically handles XP and achievement checks

## Error Handling

- If `progress.json` doesn't exist: Create it with default schema
- If JSON is invalid: Notify user and offer to reset
- If lesson already completed: Don't award duplicate XP, but allow re-reading content
- If achievement already earned: Silently skip (no error)

## Example Interactions

**User:** "Show my progress"

**Agent Response:**
```
╔═══════════════════════════════════════════════════════╗
║              📊 YOUR LEARNING PROGRESS                ║
╠═══════════════════════════════════════════════════════╣
║  Level: intermediate                                  ║
║  Current Lesson: 5                                    ║
║  Total XP: 100 ✨                                     ║
╠═══════════════════════════════════════════════════════╣
║  LESSONS                                              ║
║  ✅ Lesson 1: Introduction to Copilot Chat (25 XP)   ║
║  ✅ Lesson 2: Effective Prompting (25 XP)            ║
║  ✅ Lesson 3: Slash Commands (25 XP)                 ║
║  ✅ Lesson 4: Chat Participants (@workspace, @terminal) (25 XP) ║
║  → Lesson 5: Copilot CLI Fundamentals (current)      ║
║  ○ Lesson 6: Agentic Workflows in CLI                ║
║  ...                                                  ║
╠═══════════════════════════════════════════════════════╣
║  ACHIEVEMENTS (2/8)                                   ║
║  🎯 First Steps                                       ║
║  💬 Chat Master                                       ║
║  💯 Century Club                                      ║
╠═══════════════════════════════════════════════════════╣
║  Progress: [████████░░░░░░░░] 40%                    ║
║  Next milestone: CLI Pro (3 lessons away)            ║
╚═══════════════════════════════════════════════════════╝
```

**User:** "How much XP do I have?"

**Agent Response:**
> You have **100 XP** ✨
> 
> - Lessons completed: 4
> - Next lesson (5) will earn you 50 XP
> - 400 XP away from Power Learner achievement ⚡

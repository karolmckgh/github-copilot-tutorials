# Contributing to GitHub Copilot Tutorials

## Welcome

Thanks for your interest in contributing! 🎉

This project is an interactive, gamified tutorial that teaches developers how to use GitHub Copilot through hands-on lessons. It's built entirely on Copilot-native infrastructure — a tutorial skill (`.github/skills/tutorial/SKILL.md`), verification skills (`.github/skills/verify-lesson/`), and a progression system (`progress.json`). Lessons live in `lessons/chat/` and `lessons/cli/`, and each one awards XP upon completion.

Whether you're adding a new lesson, fixing a typo, or improving an exercise, this guide will help you contribute effectively.

## How to Add a New Lesson

### Lesson File Template

Every lesson must follow this structure:

```markdown
# Lesson N: Title

> **XP:** [25|50|100] | **Difficulty:** [Beginner|Intermediate|Advanced] | **Time:** [duration]

## Learning Objectives

## [Content Sections]

## Exercise: [Title]

### Your Task

### Steps

### Example Output

### Bonus Challenges

## Verification

## Quick Reference Card

## Summary

## Next Steps
```

- **Learning Objectives** — bullet list of what the learner will be able to do.
- **Content Sections** — teach the concepts with examples, tables, and code blocks.
- **Exercise** — a single, focused task that produces a verifiable artifact.
- **Verification** — explain what the verify skill checks (file existence, content, format).
- **Quick Reference Card** — ASCII box art summarizing key commands or concepts.
- **Summary** — brief recap of what was covered.
- **Next Steps** — tease the next lesson to keep momentum.

### Step-by-Step Process

1. **Choose lesson number and topic** — lessons are numbered sequentially across tracks (e.g., chat lessons are 01–04, CLI lessons are 05–10). Pick the next available number.
2. **Create the lesson file** in `lessons/<track>/NN-topic.md` — use lowercase, hyphen-separated slugs (e.g., `lessons/cli/11-debugging.md`).
3. **Create an exercise directory** if needed — exercises go in `exercises/<track>/`. Add a `.gitkeep` if the directory should exist before the learner creates files.
4. **Add verification criteria** to `.github/skills/verify-lesson/SKILL.md` — define what file the exercise produces, minimum content length, and any format checks.
5. **Update the lesson titles table** in the verify-lesson skill — add the new lesson number, title, and XP value to the lookup table.
6. **Add the lesson to the tutorial skill's lesson structure table** in `.github/skills/tutorial/SKILL.md` — include lesson number, file path, title, and XP.
7. **Update the README lesson table** — add a row with lesson number, title, description, and XP.
8. **Test the lesson yourself** — follow the full flow end-to-end (see [Testing Locally](#testing-locally)).

### XP Guidelines

| Difficulty   | Typical Duration | XP  |
| ------------ | ---------------- | --- |
| Beginner     | 10–15 min        | 25  |
| Intermediate | 20–25 min        | 50  |
| Advanced     | 30+ min          | 100 |

### Exercise Design Principles

- **Achievable in 5–15 minutes** — exercises should feel rewarding, not exhausting.
- **Produce a verifiable file artifact** — the verify skill checks for a specific file with expected content.
- **Include example output** — show learners what a correct result looks like.
- **Add bonus challenges for advanced learners** — optional stretch goals that go beyond the core task.
- **Don't require external services** — everything should work with just Copilot and the local repo.

## How to Report Issues

Use [GitHub Issues](../../issues) to report problems. Please include:

- **Lesson number** — which lesson is affected.
- **Expected behavior** — what should happen.
- **Actual behavior** — what actually happens.
- **Environment** — IDE, Copilot version, OS (if relevant).

## How to Suggest Improvements

- **Open an issue first** to discuss the change before investing time in a PR.
- **PRs are welcome** for typos, clarity improvements, better examples, and small fixes.
- For larger changes (new lessons, restructuring), please get alignment in an issue first.

## Style Guide

- **ATX headers** — use `#` syntax, not underline syntax.
- **Fenced code blocks** with language tags — always specify the language (` ```markdown `, ` ```bash `, ` ```json `, etc.).
- **Tables** for comparisons and structured data.
- **ASCII box art** for quick reference cards — keep them readable in any monospace font.
- **Friendly, encouraging tone** — the audience is developers learning something new.
- **Emoji sparingly** — use in section headers and callouts (✅, 💡, 🎯), not in body text.
- **Second person** — address the reader as "you."
- **Active voice** — "Click the button" not "The button should be clicked."

## Testing Locally

Before submitting a new lesson, verify the full flow works:

1. **Follow the lesson yourself** — read it start to finish and complete every step.
2. **Complete the exercise** — produce the expected artifact in the correct location.
3. **Run the verification** — ask the tutorial agent to `verify` or `verify lesson N` and confirm it passes.
4. **Check that `progress.json` updates correctly** — XP should increment, the lesson should be marked complete, and any achievements should trigger.
5. **Verify the tutorial agent recognizes the new lesson** — run `lesson N` and `outline` to confirm the lesson appears in the curriculum.

## Code of Conduct

We're committed to providing a welcoming and respectful environment for everyone. Be kind, be constructive, and assume good intent. Harassment, dismissive language, and disrespectful behavior will not be tolerated. Let's build something great together. 💙

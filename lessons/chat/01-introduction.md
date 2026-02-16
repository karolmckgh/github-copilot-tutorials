# Lesson 1: Introduction to Copilot Chat

**XP: 25** | **Difficulty: Beginner** | **Time: 10-15 minutes**

---

## 🎯 Learning Objectives

By the end of this lesson, you will:
- Understand what GitHub Copilot Chat is and how it differs from code completions
- Know how to access Copilot Chat across different platforms
- Have your first successful conversation with Copilot

---

# Part 1: Key Concepts

## 🤖 What is GitHub Copilot Chat?

Think of GitHub Copilot Chat as your AI pair programmer—one you can actually talk to! While regular Copilot suggests code as you type, Copilot Chat lets you have a conversation about your code.

**You can ask it to:**
- 📖 Explain confusing code in plain English
- 🐛 Help debug errors and suggest fixes
- ✨ Generate new code from descriptions
- 🔄 Refactor and improve existing code
- 📝 Write tests, documentation, and more

## 🧠 How Does It Work?

Two things make Copilot Chat powerful:

1. **Context Awareness** — When you ask about code in your editor, Copilot Chat knows what you're looking at. It reads the file you have open, sees your selection, and gives relevant, specific answers — not generic ones.

2. **Conversation Memory** — You can follow up with more questions and Copilot remembers what you were just talking about. It's a real conversation, not one-off queries.

## 🔑 Where to Access Copilot Chat

Copilot Chat is available in several places—use whichever works best for you!

### VS Code (Most Popular)

1. **Chat Panel**: Click the Copilot icon in the sidebar (or press `Ctrl+Shift+I` / `Cmd+Shift+I`)
2. **Inline Chat**: Press `Ctrl+I` / `Cmd+I` while in the editor to chat about specific code
3. **Quick Chat**: Press `Ctrl+Shift+P` and type "Copilot Chat"

### GitHub Copilot CLI

From your terminal, you can use:
```bash
gh copilot explain "git rebase -i HEAD~3"
gh copilot suggest "find all large files in this repo"
```

### GitHub.com

When browsing code on GitHub.com, look for the Copilot icon to ask questions about any repository!

---

# Part 2: Exercise

## ✏️ Your First Copilot Conversation

Time to try it out! You'll ask Copilot to explain a piece of code and save the result.

### Step 1: Apply Sample Code to the Editor

Here's a sample code snippet:

```python
def calculate_total(items):
    total = 0
    for item in items:
        if item['in_stock']:
            total += item['price'] * item['quantity']
    return total
```

**Hover over the code block above** — you'll see a row of icons appear in the top-right corner. Click the first icon, **"Apply in Editor"**, to insert the code into a new editor tab automatically. No copy-pasting needed!

> 💡 **Tip:** This "Apply in Editor" button works on any code block Copilot shows you — it's one of the most useful features in Copilot Chat!

### Step 2: Select the Code

In the editor tab where the code was applied, highlight the code (or just place your cursor in the function).

### Step 3: Ask Copilot to Explain It

Open the Chat panel and type a question like:

> "Can you explain what this function does?"

Or try:

> "What would happen if items is empty?"

Notice how Copilot:
- Breaks down the logic step by step
- Uses the actual variable names from your code
- Might even suggest improvements!

### Step 4: Verify Your Work

Once you've had your conversation with Copilot, simply say **"verify"** in the chat.

Copilot will automatically save your conversation to `exercises/chat/01-result.md` and confirm your completion!

> 🎯 **Bonus challenge:** Before verifying, try a follow-up question in the same conversation (e.g. "How would you add a discount parameter?") — it'll be included in your saved result too!

---

## ✅ Verification

Just say **"verify"** when you're ready! Copilot will:

- [ ] Save your conversation to `exercises/chat/01-result.md` automatically
- [ ] Check that everything looks good
- [ ] Award you XP for completing the lesson!

---

## 🎉 You Did It!

Congratulations on your first Copilot Chat conversation! You've just unlocked a powerful tool that can help you:
- Learn faster by getting instant explanations
- Code more confidently with an AI partner
- Solve problems through conversation

**What's Next?** In the next lesson, we'll explore how to ask better questions and get more useful responses from Copilot Chat.

---

## 📚 Additional Resources

- [GitHub Copilot Chat Documentation](https://docs.github.com/en/copilot/github-copilot-chat)
- [VS Code Copilot Chat Guide](https://code.visualstudio.com/docs/copilot/copilot-chat)
- [Copilot CLI Documentation](https://docs.github.com/en/copilot/github-copilot-in-the-cli)

---

*Keep experimenting! The more you chat with Copilot, the better you'll understand how to get the help you need. You've got this! 🚀*

## Next Steps

Continue to [Lesson 2: Effective Prompting](./02-prompting.md) to learn how to write better prompts for more useful Copilot responses.

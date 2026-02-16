# Lesson 2: Effective Prompting

**XP: 25** | **Difficulty: Beginner** | **Time: 15-20 minutes**

---

## 🎯 Learning Objectives

By the end of this lesson, you will:
- Understand what makes a good prompt vs. a weak prompt
- Learn the CRISPE framework for structuring powerful prompts
- Practice iterating on prompts to get better results

---

## 💡 Why Prompts Matter

Here's a secret: **the quality of your prompt directly determines the quality of Copilot's response**.

Think of it like giving directions. Compare these two:

❌ **Vague:** "Go to the store"  
✅ **Clear:** "Drive to the Whole Foods on Main Street, park in the back lot, and buy the organic bananas near the entrance"

The same principle applies to Copilot Chat. Better prompts = better results.

### Real Example

Let's see this in action with a coding task:

**Weak Prompt:**
> "Make this code better"

**Strong Prompt:**
> "Refactor this function to improve readability: use descriptive variable names, add input validation, and split the nested conditionals into separate helper functions. Keep the same functionality."

The first prompt might give you *something*, but the second tells Copilot exactly what "better" means to you!

---

## 🔬 Anatomy of a Good Prompt

Every effective prompt has three core elements:

### 1. Context 📍
Tell Copilot what you're working on and why.

```
"I'm building a REST API for a todo app..."
"This is a React component that displays user profiles..."
"I'm optimizing this database query for performance..."
```

### 2. Specificity 🎯
Be precise about what you want. Vague requests get vague responses.

| Vague ❌ | Specific ✅ |
|----------|-------------|
| "Fix this code" | "Fix the null pointer exception on line 15" |
| "Make it faster" | "Reduce time complexity from O(n²) to O(n)" |
| "Add comments" | "Add JSDoc comments with @param and @returns" |

### 3. Examples 📝
When possible, show Copilot what you want.

```
"Format the output like this:
- User: John Doe
- Email: john@example.com
- Status: Active"
```

---

## 🏗️ The CRISPE Framework

For complex requests, use the **CRISPE framework**. It's optional but powerful when you need precise results.

| Letter | Meaning | Example |
|--------|---------|---------|
| **C** | **Context** | "I'm working on a Node.js Express API" |
| **R** | **Role** | "Act as a senior backend developer" |
| **I** | **Instructions** | "Refactor this function to use async/await" |
| **S** | **Specificity** | "Handle errors with try/catch, return proper HTTP status codes" |
| **P** | **Persona** | "Explain your changes as if I'm a junior developer" |
| **E** | **Examples** | "Similar to how the /users endpoint is structured" |

### CRISPE in Action

Here's a complete CRISPE prompt:

> **Context:** I'm building an e-commerce checkout system in Python.
>
> **Role:** Act as a senior Python developer with expertise in payment systems.
>
> **Instructions:** Review this payment processing function and identify security vulnerabilities.
>
> **Specificity:** Focus on input validation, SQL injection risks, and sensitive data handling. List each issue with severity (high/medium/low).
>
> **Persona:** Explain the issues clearly so I can learn why they're dangerous.
>
> **Examples:** Format your response like:
> - 🔴 HIGH: [Issue] - [Why it's dangerous] - [How to fix]

You don't need *every* element for *every* prompt, but knowing them helps when you're stuck!

---

## ⚠️ Common Pitfalls

Avoid these common mistakes that lead to poor results:

### 1. The Vague Request
❌ "Help me with this code"  
✅ "Help me understand why this async function returns undefined instead of the API response"

### 2. Missing Context
❌ "Convert this to TypeScript"  
✅ "Convert this JavaScript React component to TypeScript. The component receives a `user` object with `id` (number) and `name` (string) properties."

### 3. Asking Multiple Things at Once
❌ "Fix the bug, add tests, improve performance, and add documentation"  
✅ Break it into separate requests—one at a time gets better results

### 4. Assuming Copilot Knows Your Codebase
❌ "Use the same pattern as our other services"  
✅ "Use dependency injection pattern: pass dependencies as constructor parameters rather than importing directly"

### 5. Not Iterating
Your first prompt might not be perfect—that's okay! Follow up with:
- "Can you make that more concise?"
- "Actually, use arrow functions instead"
- "Show me an alternative approach"

---

## 🔄 The Iteration Loop

Great prompts often come from iteration:

```
┌─────────────────────────────────────────┐
│  1. Start with a reasonable prompt      │
│              ↓                          │
│  2. Review Copilot's response           │
│              ↓                          │
│  3. Identify what's missing or wrong    │
│              ↓                          │
│  4. Refine your prompt with more detail │
│              ↓                          │
│  5. Repeat until satisfied              │
└─────────────────────────────────────────┘
```

**Example iteration:**

1. **You:** "Add error handling"
2. **Copilot:** *Adds basic try/catch*
3. **You:** "Also log the errors and return user-friendly messages"
4. **Copilot:** *Improves the code*
5. **You:** "Perfect, but use our logger utility instead of console.log"
6. **Copilot:** *Final refined version*

---

## ✏️ Exercise: Refactor with Good Prompting

Now let's practice! Your task is to refactor messy code using effective prompting techniques.

### The Code to Refactor

Here's a function that's hard to read and maintain:

```javascript
function calc(a,b,c,d) {
  if(a>0){if(b>0){return a*b+c-d}else{return a-b+c*d}}else{return 0}
}
```

### Your Mission

1. **Open Copilot Chat** in VS Code (or your preferred editor)
2. **Craft a good prompt** using what you learned:
   - Provide context (what is this function supposed to do?)
   - Be specific (what improvements do you want?)
   - Give examples if helpful (how should variables be named?)
3. **Iterate** if the first response isn't quite right
4. **Say "verify"** — Copilot will automatically save your refactored code to `exercises/chat/02-refactored.js`

### Hints for Your Prompt

Think about asking Copilot to:
- Use descriptive variable and function names
- Format the code properly with clear indentation
- Simplify the nested if-statements
- Add comments explaining the logic
- Consider edge cases

### Example Starting Prompt

Here's one way to start (but feel free to write your own!):

> "Refactor this JavaScript function to be more readable. The function appears to calculate something based on four numeric inputs, but the logic is unclear. Please:
> 1. Use descriptive names for parameters and the function
> 2. Break down the nested conditionals into clear, separate conditions
> 3. Add a brief comment explaining what the function does
> 4. Keep the exact same logic/output"

---

## ✅ Verification

You've completed this lesson when you say **"verify"**. Copilot will:

1. Review your conversation history for refactored code
2. Auto-save it to `exercises/chat/02-refactored.js`
3. Verify the file exists and contains readable, refactored code
4. Award your XP! 🎉

> 💡 **Note:** You must have refactored the code with Copilot before verifying. If no refactored code is found in the conversation, you'll be asked to complete the exercise first.

---

## 🎉 Key Takeaways

You've learned the art of effective prompting! Remember:

| Principle | Why It Matters |
|-----------|----------------|
| **Be Specific** | Vague prompts get vague results |
| **Provide Context** | Copilot can't read your mind |
| **Use Examples** | Show, don't just tell |
| **Iterate** | Great prompts evolve through conversation |
| **Try CRISPE** | When you need precise, complex results |

---

## 📚 Additional Resources

- [GitHub's Prompt Engineering Guide](https://docs.github.com/en/copilot/using-github-copilot/prompt-engineering-for-github-copilot)
- [Best Practices for Copilot Chat](https://docs.github.com/en/copilot/github-copilot-chat/copilot-chat-in-ides/using-github-copilot-chat-in-your-ide)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)

---

## 🚀 What's Next?

Now that you know how to craft effective prompts, you're ready to tackle more advanced Copilot Chat features. In the next lesson, we'll explore chat participants and slash commands that give you even more control!

---

*Remember: prompting is a skill that improves with practice. Don't be afraid to experiment, iterate, and find what works best for you! 💪*

## Next Steps

Continue to [Lesson 3: Slash Commands](./03-slash-commands.md) to learn powerful built-in commands like /fix, /explain, /tests, and /doc.

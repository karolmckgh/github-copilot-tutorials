# Lesson 9: Building an MCP Tool

> **XP:** 100 | **Difficulty:** Advanced | **Time:** 35 minutes

## Learning Objectives

By the end of this lesson, you will:
- Understand what MCP (Model Context Protocol) is and why it matters
- Know the architecture: transports, servers, and tools
- Configure MCP servers in `.copilot/mcp-config.json`
- Build a custom MCP tool from scratch (Node.js or Python)
- See how this entire tutorial uses every concept you've learned

---

## What is MCP?

**Model Context Protocol (MCP)** is an open standard that lets AI assistants like Copilot connect to external tools and data sources. Think of it as a **universal plug system** for AI — any tool that speaks MCP can work with any AI that supports it.

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│              │     │              │     │              │     │              │
│  Copilot CLI │◄───►│  MCP Client  │◄───►│  MCP Server  │◄───►│  Your Data   │
│  (the AI)    │     │  (built-in)  │     │  (your tool) │     │  & Systems   │
│              │     │              │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
     You ask            Copilot              Your code          Databases, APIs,
     a question         routes it            processes it       files, services
```

**Without MCP**, Copilot can only work with what's in your files and its training data. **With MCP**, Copilot can query databases, check monitoring dashboards, trigger deployments, search knowledge bases, and anything else you can build.

### Why MCP Matters

| Without MCP | With MCP |
|-------------|----------|
| Copy-paste data into prompts | Copilot queries data directly |
| Limited to file context | Access any system or API |
| Manual tool switching | Tools available in conversation |
| Static knowledge only | Live, real-time information |
| Same tools for everyone | Custom tools for your workflow |

### Real-World MCP Examples

Here's what teams are building with MCP:

| Use Case | What It Does |
|----------|-------------|
| 🗄️ **Database Explorer** | Query production databases, explain schemas, find records |
| 📊 **Monitoring** | Check service health, pull metrics, diagnose incidents |
| 🚀 **Deployment** | Trigger deploys, check pipeline status, roll back changes |
| 📚 **Knowledge Base** | Search internal docs, wikis, runbooks, and FAQs |
| 🧪 **Testing** | Run test suites, analyze coverage, find flaky tests |
| 🔐 **Secrets Manager** | Safely reference secrets without exposing values |
| 📦 **Package Registry** | Search internal packages, check versions, find dependencies |

---

## MCP Architecture

### How It Works

When you use an MCP tool in Copilot, here's what happens:

1. **You ask a question** — "What's the status of our production database?"
2. **Copilot recognizes the tool** — It sees an MCP server that can answer this
3. **MCP Client sends a request** — The built-in client calls your MCP server
4. **Your server processes it** — Runs a query, calls an API, reads a file, etc.
5. **Results flow back** — Your server returns structured data to Copilot
6. **Copilot formats the answer** — Presents the results in natural language

The key insight: **you write the server**, and Copilot handles everything else.

### MCP Transports

MCP servers communicate with Copilot using one of two transports:

| Feature | stdio (Local) | SSE (Remote) |
|---------|--------------|--------------|
| **How it runs** | Subprocess on your machine | HTTP server (local or remote) |
| **Connection** | stdin/stdout pipes | Server-Sent Events over HTTP |
| **Best for** | Local tools, file access | Shared team tools, remote APIs |
| **Setup** | Just a command to run | Needs a running HTTP server |
| **Security** | Runs as your user | Needs auth/network config |
| **Example** | CLI tool, script | Team dashboard, shared DB tool |

**Most tools start with stdio** because it's simpler — your tool is just a script that Copilot runs as a subprocess.

---

## MCP Configuration

### The Configuration File

MCP servers are configured in `.copilot/mcp-config.json` at the root of your repository (or in your home directory for global tools).

### Basic Structure

```json
{
  "servers": {
    "my-tool": {
      "type": "stdio",
      "command": "node",
      "args": ["./tools/my-mcp-server.js"],
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

### Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `type` | Yes | Transport type: `"stdio"` or `"sse"` |
| `command` | Yes (stdio) | The command to run the server |
| `args` | No | Array of command-line arguments |
| `env` | No | Environment variables to pass to the server |
| `url` | Yes (sse) | URL of the SSE server endpoint |

### Multiple Servers

You can configure as many servers as you need:

```json
{
  "servers": {
    "database": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "mydb.sqlite"]
    },
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./data"]
    },
    "custom-tool": {
      "type": "stdio",
      "command": "python3",
      "args": ["./tools/my-tool.py"]
    }
  }
}
```

> 💡 **Pro Tip:** Start with one server, verify it works, then add more. Debugging multiple new servers at once is painful!

---

## Building Your First MCP Tool

Let's build a real MCP tool that Copilot can use. We'll create a **project-stats** tool that counts files by extension — useful for understanding any codebase at a glance.

### Option A: Node.js (Full Example)

First, initialize the project and install the SDK:

```bash
mkdir -p tools && cd tools
npm init -y
npm install @modelcontextprotocol/sdk
```

Create `tools/project-stats.js`:

```javascript
#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { readdirSync, statSync } from "fs";
import { join, extname } from "path";

// Create the MCP server
const server = new McpServer({
  name: "project-stats",
  version: "1.0.0",
});

// Helper: recursively count files by extension
function countFiles(dir, counts = {}, depth = 0) {
  if (depth > 10) return counts; // prevent infinite recursion
  try {
    const entries = readdirSync(dir);
    for (const entry of entries) {
      if (entry.startsWith(".") || entry === "node_modules") continue;
      const fullPath = join(dir, entry);
      const stat = statSync(fullPath);
      if (stat.isDirectory()) {
        countFiles(fullPath, counts, depth + 1);
      } else {
        const ext = extname(entry) || "(no extension)";
        counts[ext] = (counts[ext] || 0) + 1;
      }
    }
  } catch (e) {
    // skip directories we can't read
  }
  return counts;
}

// Register the "count_files" tool
server.tool(
  "count_files",
  "Count files in a directory grouped by extension",
  {
    directory: z.string().optional().describe(
      "Directory to scan (defaults to current directory)"
    ),
  },
  async ({ directory }) => {
    const dir = directory || process.cwd();
    const counts = countFiles(dir);

    // Sort by count descending
    const sorted = Object.entries(counts)
      .sort(([, a], [, b]) => b - a);

    const total = sorted.reduce((sum, [, count]) => sum + count, 0);

    let result = `Project Statistics for: ${dir}\n`;
    result += `${"─".repeat(40)}\n`;
    for (const [ext, count] of sorted) {
      const bar = "█".repeat(Math.min(count, 30));
      result += `${ext.padEnd(16)} ${String(count).padStart(5)}  ${bar}\n`;
    }
    result += `${"─".repeat(40)}\n`;
    result += `Total files: ${total}\n`;

    return {
      content: [{ type: "text", text: result }],
    };
  }
);

// Start the server
const transport = new StdioServerTransport();
await server.connect(transport);
```

> 📝 **Note:** Make sure your `tools/package.json` has `"type": "module"` for ES module imports, or use CommonJS `require()` syntax instead.

### Option B: Python (Simpler Example)

Install the Python MCP SDK:

```bash
pip install mcp
```

Create `tools/project_stats.py`:

```python
#!/usr/bin/env python3
"""MCP server that provides project file statistics."""

import os
from collections import Counter
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("project-stats")


@mcp.tool()
def count_files(directory: str = ".") -> str:
    """Count files in a directory grouped by file extension."""
    counts = Counter()

    for root, dirs, files in os.walk(directory):
        # Skip hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules"]
        for f in files:
            if f.startswith("."):
                continue
            ext = os.path.splitext(f)[1] or "(no extension)"
            counts[ext] += 1

    total = sum(counts.values())
    lines = [f"Project Statistics for: {os.path.abspath(directory)}"]
    lines.append("─" * 40)
    for ext, count in counts.most_common():
        bar = "█" * min(count, 30)
        lines.append(f"{ext:<16} {count:>5}  {bar}")
    lines.append("─" * 40)
    lines.append(f"Total files: {total}")

    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Configuring Your Tool

After building the tool, add it to `.copilot/mcp-config.json`:

**For Node.js:**
```json
{
  "servers": {
    "project-stats": {
      "type": "stdio",
      "command": "node",
      "args": ["./tools/project-stats.js"]
    }
  }
}
```

**For Python:**
```json
{
  "servers": {
    "project-stats": {
      "type": "stdio",
      "command": "python3",
      "args": ["./tools/project_stats.py"]
    }
  }
}
```

Once configured, you can ask Copilot things like:
- *"Use project-stats to count the files in this repo"*
- *"How many Python files are in the tools directory?"*
- *"Give me a breakdown of file types in this project"*

Copilot will automatically invoke your MCP tool to answer!

---

## The Meta Moment 🤯

Here's something mind-bending: **this tutorial you're completing right now uses every concept from all 9 lessons.** Let that sink in.

| Concept | Lesson | How This Tutorial Uses It |
|---------|--------|--------------------------|
| Chat basics | 1 | You chatted with Copilot throughout |
| Prompt engineering | 2 | Exercises taught you to craft better prompts |
| Slash commands | 3 | `/explain`, `/fix`, `/tests` in exercises |
| Participants | 4 | `@workspace` to explore the repo |
| CLI fundamentals | 5 | Running `copilot` in your terminal |
| Agentic workflows | 6 | Multi-step tasks with autonomous execution |
| Advanced agentic | 7 | Fleet mode, subagents, and TDD |
| Custom instructions | 8 | `.github/copilot-instructions.md` shapes behavior |
| **MCP tools** | **9** | **Extending Copilot with external capabilities** |

You didn't just learn features in isolation — you experienced a system where **instructions guide behavior**, **agents define roles**, and **MCP tools extend capabilities**. That's the full Copilot customization stack.

---

## Exercise: Configure an MCP Tool

### Your Task

Set up an MCP configuration file so Copilot knows about at least one MCP server. This is the foundation for extending Copilot with custom tools.

### Steps

1. **Create the `.copilot/` directory** in the repository root:
   ```bash
   mkdir -p .copilot
   ```

2. **Create `.copilot/mcp-config.json`** with at least one server configured.

3. **Choose one of these approaches:**

   **Option A — Use an existing MCP server package:**
   ```bash
   # Example: SQLite MCP server (no code needed!)
   npx -y @modelcontextprotocol/server-sqlite --help
   ```

   **Option B — Create a custom tool:**
   Build the project-stats tool from the examples above.

   **Option C — Let Copilot help you:**
   ```
   "Help me create an MCP server that [describes what you want]"
   ```

4. **Verify** your JSON is valid and contains a `servers` key.

### Example Configuration

```json
{
  "servers": {
    "project-stats": {
      "type": "stdio",
      "command": "node",
      "args": ["./tools/project-stats.js"]
    }
  }
}
```

### Bonus Challenges

- Add a second MCP server to your configuration (e.g., filesystem or SQLite)
- Build a custom MCP tool that does something useful for your workflow
- Add environment variables to your server configuration
- Try configuring an SSE-based remote server

---

## Verification

To complete this lesson, you need:

**The following file must exist with valid configuration:**
- `.copilot/mcp-config.json` (valid JSON with a `servers` key)

Run the verification:

```bash
python3 -c "
import json, sys
try:
    with open('.copilot/mcp-config.json') as f:
        cfg = json.load(f)
    if 'servers' in cfg and len(cfg['servers']) > 0:
        print('✅ MCP configuration is valid!')
        for name in cfg['servers']:
            print(f'   Server: {name}')
    else:
        print('❌ Config needs a \"servers\" key with at least one server')
except FileNotFoundError:
    print('❌ .copilot/mcp-config.json not found')
except json.JSONDecodeError:
    print('❌ Invalid JSON in .copilot/mcp-config.json')
"
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│                   MCP TOOLS                             │
├─────────────────────────────────────────────────────────┤
│  Config:  .copilot/mcp-config.json                     │
│                                                         │
│  Transports:                                            │
│    stdio  →  Local subprocess (command + args)          │
│    sse    →  Remote HTTP server (url)                   │
│                                                         │
│  Minimal Config:                                        │
│  {                                                      │
│    "servers": {                                         │
│      "my-tool": {                                      │
│        "type": "stdio",                                │
│        "command": "node",                              │
│        "args": ["./tool.js"]                           │
│      }                                                  │
│    }                                                    │
│  }                                                      │
├─────────────────────────────────────────────────────────┤
│  Building Tools:                                        │
│    Node.js  →  @modelcontextprotocol/sdk                │
│    Python   →  pip install mcp                          │
│                                                         │
│  Key Steps:                                             │
│    1. Create server with SDK                            │
│    2. Register tools with name + schema                 │
│    3. Connect via StdioServerTransport                  │
│    4. Add to mcp-config.json                            │
├─────────────────────────────────────────────────────────┤
│  Pro Tips:                                              │
│  • Start with stdio, upgrade to SSE if needed           │
│  • Test your server standalone before configuring       │
│  • Use env field for secrets (never hardcode!)          │
│  • Check the MCP ecosystem for existing servers         │
└─────────────────────────────────────────────────────────┘
```

---

## Summary

| Topic | Key Point |
|-------|-----------|
| What MCP is | Open standard for AI tool extensibility |
| Why it matters | Connect Copilot to any data source or system |
| Transports | stdio (local, simple) and SSE (remote, shared) |
| Configuration | `.copilot/mcp-config.json` with a `servers` key |
| Building tools | Use `@modelcontextprotocol/sdk` (Node.js) or `mcp` (Python) |
| The full stack | Instructions → MCP Tools |

**Key Takeaways:**
- MCP is an **open standard** — tools you build work across MCP-compatible AI systems
- Start with **stdio** transport for local tools, use **SSE** for shared/remote tools
- The **configuration is simple** — just JSON pointing to a command
- Building a tool is **surprisingly easy** — a working server can be under 50 lines
- MCP completes the customization duo: **instructions** (behavior) and **tools** (capabilities)

---

## 🎉 Congratulations!

You've completed all 9 lessons! Here's what you've mastered:

| Track | Lessons | What You Learned |
|-------|---------|-----------------|
| **Chat** | 1-4 | Chat basics, prompting, commands, participants |
| **CLI** | 5-7 | CLI fundamentals, agentic workflows |
| **Customization** | 8-9 | Instructions, MCP tools |

### What's Next?

- 🏆 Check your progress and achievements
- 🛠️ Apply what you learned to real projects
- 👥 Share this tutorial with your team
- 🤖 Create custom agents and MCP tools for your workflow

**You didn't just learn Copilot — you learned it *from* Copilot. Now go build amazing things! 🚀**

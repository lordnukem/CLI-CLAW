# AutonomousClaw

A CLI-first, fully autonomous software development orchestrator designed to eliminate the need for human intervention in the development lifecycle.

## Overview
AutonomousClaw coordinates a swarm of specialized AI agents to manage end-to-end software projects through autonomous sprint cycles. It pivots toward a "Zero-Human" orchestration model, utilizing a local state machine to orchestrate tasks between simulated roles:
- **Product Owner**
- **Architect & Developer**
- **QA Engineer**
- **Integrator**

It is designed to be lightweight, utilizing standard REST interfaces to connect with OpenAI-compatible endpoints without requiring heavy C++ or Rust build tools.

## Prerequisites
- **Python:** 3.10+
- **OpenAI API Key** (Or an API Key to an OpenAI compatible endpoint like Groq or LocalLLM).

## Installation

```powershell
# 1. Clone the repository and enter the directory (if you haven't already)
git clone <your-repo>
cd CLI-Claw

# 2. Create and activate a Virtual Environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # On Windows

# 3. Install dependencies
pip install -r requirements.txt
pip install -e .
```

## Configuration

Set up your environment variables before running the CLI. By default, it uses `gpt-4o` and points to the official OpenAI API unless otherwise specified.

```powershell
$env:OPENAI_API_KEY="sk-your-real-key"

# Optional Overrides for Local LLMs or different providers:
$env:CLAW_API_BASE="https://api.openai.com/v1"
$env:CLAW_DEFAULT_MODEL="gpt-4o"
```

## Usage Guide

AutonomousClaw operates on the concept of **Sprints**. A sprint is instantiated by the Product Owner and then automatically worked on by the Swarm.

### 1. Start a New Sprint
Give a high-level project goal. The Product Owner Agent will connect to the LLM, break the goal down into technical task criteria, and initialize the local `.claw_state.json` Sprint Backlog.

```powershell
python autonomous_claw/cli.py start "Build a Python script that scrapes HackerNews top 10 articles and saves them to a CSV file."
```

### 2. View Sprint Status
Check the current state of "Our Plan" to see what tasks are Queued (`TODO`), `IN PROGRESS`, `DONE`, or `VERIFIED` (by QA).

```powershell
python autonomous_claw/cli.py status
```

### 3. Let the Agents Work (Zero-Human Loop)
Invoke the **Integrator** agent. The Integrator will take control of your terminal and iteratively trigger the Developer to write the code (using its `Code Skill` to execute local shell commands natively) and then hand it to the QA Engineer to write and run tests against the developer's work.

*The Integrator will stop when all tasks are Verified, or it runs out of iterations.*

```powershell
# Run the autonomous loop for up to 5 iterative steps
python autonomous_claw/cli.py auto --iterations 5
```

### 4. Direct Manual Agent Trigger (Optional)
If you want to step through the system manually without the Integrator taking full control, you can force the Developer or active agent to pull the top task and execute it one step at a time:

```powershell
python autonomous_claw/cli.py act
```

## Technical Flow
1. **Agent State**: Handled natively in `.claw_state.json`.
2. **Code Skills**: Agents are prompted with the ability to emit ```bash ... ``` context blocks. The system extracts this and executes it in your literal terminal. 
3. **Gemini CLI / Claude Code Integration**: Because agents execute standard shell commands, they can leverage CLI tools installed on your system. If you want the agent to rely on Google's Gemini CLI or Anthropic's Claude Code, prompt the Sprint Goal to include: "Use the `gemini` CLI" or "Use the `claude` CLI." The Developer Agent knows how to delegate recursive tasks to these local CLI bots natively!

---
*Built with Typer, Python, and the Autonomous Swarm Philosophy.*

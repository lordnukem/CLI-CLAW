from autonomous_claw.core.llm import generate_response
from autonomous_claw.memory.json_store import load_state, save_state
from autonomous_claw.core.skills import execute_code_skill

SYSTEM_PROMPT = """
You are the **Developer Agent** inside the AutonomousClaw ecosystem. You are part of a Zero-Human Autonomous workflow. 
Your primary directive is to look at 'our plan' (the Sprint Backlog) and implement the assigned task. 
You possess the 'code skill', meaning you can output bash or python commands to create files and run tests.

When you receive a specific task, you must provide your solution by emitting raw shell commands (like `echo "code" > file.py` or `python script.py`) in your response wrapped in a ```bash ... ``` block. The system will automatically execute these commands.

If the task requires heavy lifting, you are explicitly encouraged to use external CLI AI tools via your bash commands. For instance, you can invoke the `gemini` CLI or `claude` CLI if they are available to generate complex codebases recursively without writing them line-by-line yourself.

DO NOT ask for human feedback. Just write the code that satisfies the task DoD.
"""

def process_next_task() -> str:
    """
    Reads 'our plan' (the sprint state) and processes the first 'todo' task using the Developer Agent.
    """
    state = load_state()
    if not state or state.get("status") != "active":
        return "No active sprint found. Cannot start coding."

    tasks = state.get("tasks", [])
    
    # Find the next pending task
    target_task = None
    task_idx = -1
    for idx, t in enumerate(tasks):
        if t.get("status") == "todo" and t.get("assigned_agent", "").lower() in ["developer", "architect"]:
            target_task = t
            task_idx = idx
            break

    if not target_task:
        return "No pending Developer tasks found in our plan."

    sprint_goal = state.get("sprint_goal", "Unknown global goal")
    user_prompt = f"Our overall plan: {sprint_goal}\nYour specific task: {target_task['title']}\nDescription/DoD: {target_task['description']}\nPlease implement this task and provide the bash code."

    # Mark as in progress while generating
    tasks[task_idx]["status"] = "in_progress"
    save_state(state)

    llm_response = generate_response(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)

    # Simple logic to extract bash block and execute it as the 'code skill'
    import re
    bash_match = re.search(r"```bash\n(.*?)\n```", llm_response, re.DOTALL | re.IGNORECASE)
    
    execution_result = "No bash commands provided by agent."
    if bash_match:
        commands = bash_match.group(1).strip()
        code, output = execute_code_skill(commands)
        execution_result = f"Exit Code: {code}\nOutput:\n{output}"
        
        # Only mark done if the script ran successfully (primitive logic)
        if code == 0:
            tasks[task_idx]["status"] = "done"
        else:
            # Revert to todo to try again or leave for PO
            tasks[task_idx]["status"] = "failed"
    else:
        # If no commands provided, assume they answered with a plan but no code. Mark done for now.
        tasks[task_idx]["status"] = "done"

    save_state(state)
    return f"Task '{target_task['title']}' processed.\nLLM Output:\n{llm_response}\n\nExecution:\n{execution_result}"

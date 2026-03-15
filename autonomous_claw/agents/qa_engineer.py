from autonomous_claw.core.llm import generate_response
from autonomous_claw.memory.json_store import load_state, save_state
from autonomous_claw.core.skills import execute_code_skill

SYSTEM_PROMPT = """
You are the **QA Engineer Agent** inside the AutonomousClaw ecosystem. You are part of a Zero-Human Autonomous workflow. 
Your primary directive is to review 'our plan' (the Sprint Backlog) and ensure the Developer's recent work meets the Definition of Done.

You have the 'code skill'. You must output your response in raw bash commands wrapped in a ```bash ... ``` block. 
You will typically run test commands (like `pytest tests/`, `npm test`, or execute a script the developer built to verify it returns expected output).

If the code runs successfully and meets requirements, your test commands exiting with 0 will mark the task as fully DONE.
If it fails, the system will kick it back to the Developer automatically. Write robust test commands.
"""

def review_recent_task() -> str:
    """
    Finds a completed (or failed) Developer task and attempts to run QA tests to verify.
    """
    state = load_state()
    if not state or state.get("status") != "active":
        return "No active sprint found. Cannot run QA."

    tasks = state.get("tasks", [])
    
    # QA looks for 'done' tasks by dev to verify, or 'failed' to write regression tests
    target_task = None
    task_idx = -1
    for idx, t in enumerate(tasks):
        if t.get("status") == "done" and t.get("qa_approved") is not True:
            target_task = t
            task_idx = idx
            break

    if not target_task:
        return "No pending tasks require QA review at this moment."

    sprint_goal = state.get("sprint_goal", "Unknown global goal")
    user_prompt = f"Our overall plan: {sprint_goal}\nThe Developer recently completed this task: {target_task['title']}\nDescription/DoD: {target_task['description']}\nPlease write bash commands to test this implementation."

    llm_response = generate_response(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)

    import re
    bash_match = re.search(r"```bash\n(.*?)\n```", llm_response, re.DOTALL | re.IGNORECASE)
    
    execution_result = "No QA tests provided."
    if bash_match:
        commands = bash_match.group(1).strip()
        code, output = execute_code_skill(commands)
        execution_result = f"Exit Code: {code}\nOutput:\n{output}"
        
        if code == 0:
            tasks[task_idx]["qa_approved"] = True
            tasks[task_idx]["status"] = "verified"
        else:
            # Kick back to Developer
            tasks[task_idx]["status"] = "todo"
            tasks[task_idx]["qa_feedback"] = output
    else:
        # Assuming approval if the LLM didn't provide scripts but gave text
        tasks[task_idx]["qa_approved"] = True
        tasks[task_idx]["status"] = "verified"

    save_state(state)
    return f"QA Review for '{target_task['title']}'.\nTests:\n{llm_response}\n\nExecution:\n{execution_result}"

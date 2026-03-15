from autonomous_claw.core.llm import generate_response

SYSTEM_PROMPT = """
You are the **Product Owner Agent** inside the AutonomousClaw ecosystem. Your goal is to receive a high-level user prompt and break it down into an actionable **Sprint Backlog**.
You are part of a Zero-Human Autonomous workflow. The Developer and QA agents will execute this backlog immediately.

Your output must be structured as a strict JSON representing the backlog logic, followed by a human-readable summary. 
The JSON must provide individual `tasks` which have a `title`, `description` (with the definition of done), and `assigned_agent` (e.g., Developer or Architect).

CRITICAL: Provide your output exactly as requested, focusing on technical breakdown without conversational filler, starting with the raw markdown:

```json
{
  "project_goal": "...",
  "tasks": [
    {
       "title": "...",
       "description": "...",
       "assigned_agent": "Developer"
    }
  ]
}
```
"""

def generate_sprint_backlog(high_level_prompt: str, prd_content: str | None = None) -> str:
    """
    Connect to the LLM and pass the Product Owner context.
    Returns the structured Sprint Backlog text (or JSON).
    """
    if prd_content:
        user_prompt = f"Please build a backlog for the following project: {high_level_prompt}\n\nHere is the detailed Product Requirements Document (PRD):\n\n{prd_content}"
    else:
        user_prompt = f"Please build a backlog for the following project: {high_level_prompt}"

    return generate_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )

import json
import os
from typing import Dict, Any

STATE_FILE = ".claw_state.json"

def save_state(state: Dict[str, Any], filepath: str = STATE_FILE) -> None:
    """Safely writes the current state dictionary to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)

def load_state(filepath: str = STATE_FILE) -> Dict[str, Any]:
    """Loads the state dictionary from the JSON file. Returns empty dict if not found."""
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def init_new_sprint(backlog_data: Dict[str, Any]) -> None:
    """
    Initializes a new sprint state based on the Product Owner's backlog.
    """
    state = load_state()
    # Ensure there's a task structure
    tasks = backlog_data.get("tasks", [])
    for task in tasks:
        # Give every task a default state if not provided
        if "status" not in task:
            task["status"] = "todo"
            
    state["sprint_goal"] = backlog_data.get("project_goal", "Unknown Goal")
    state["tasks"] = tasks
    state["status"] = "active"
    
    save_state(state)

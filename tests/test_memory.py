import json
import os
import pytest
from autonomous_claw.memory.json_store import save_state, load_state
from autonomous_claw.core.utils import extract_json_from_markdown

TEST_STATE_FILE = ".test_claw_state.json"


@pytest.fixture(autouse=True)
def clean_state():
    yield
    if os.path.exists(TEST_STATE_FILE):
        os.remove(TEST_STATE_FILE)

def test_save_and_load_state():
    test_data = {"sprint_goal": "Test Goal", "status": "active"}
    save_state(test_data, filepath=TEST_STATE_FILE)
    
    loaded = load_state(filepath=TEST_STATE_FILE)
    assert loaded["sprint_goal"] == "Test Goal"

def test_extract_json_markdown_block():
    markdown = "Here is the output:\n```json\n{\"project_goal\": \"goal1\", \"tasks\": []}\n```\nEnjoy!"
    parsed = extract_json_from_markdown(markdown)
    assert parsed["project_goal"] == "goal1"


def test_extract_json_fallback():
    markdown = "Here is the output: {\"project_goal\": \"goal2\", \"tasks\": []} Enjoy!"
    parsed = extract_json_from_markdown(markdown)
    assert parsed["project_goal"] == "goal2"

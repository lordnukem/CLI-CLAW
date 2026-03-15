import re
import json

def extract_json_from_markdown(text: str) -> dict:
    """
    Extracts and parses a JSON object from a markdown string.
    Finds the first ```json ... ``` block or falls back to finding the first { ... }.
    """
    # Try looking for a markdown JSON block
    match = re.search(r"```(?:json)?(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        json_str = match.group(1).strip()
    else:
        # Fallback: find the first { and last }
        start = int(text.find("{"))
        end = int(text.rfind("}"))
        if start != -1 and end != -1 and end > start:
            end_idx = end + 1
            json_str = text[start:end_idx]
        else:
            raise ValueError("No JSON object found in text.")

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}\nRaw Data: {json_str}")

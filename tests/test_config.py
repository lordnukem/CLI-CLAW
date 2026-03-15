import os
from autonomous_claw.core.config import Config

def test_default_config():
    config = Config()
    assert config.default_model == "gpt-4o"
    assert config.fallback_model == "gpt-4o"
    assert config.chroma_db_path == "./.chroma"

def test_env_override():
    os.environ["CLAW_DEFAULT_MODEL"] = "qwen-2.5-coder"
    config = Config()
    assert config.default_model == "qwen-2.5-coder"
    
    # Cleanup
    del os.environ["CLAW_DEFAULT_MODEL"]

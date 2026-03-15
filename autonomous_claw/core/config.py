import os

class Config:
    @property
    def default_model(self) -> str:
        return os.environ.get("CLAW_DEFAULT_MODEL", "gpt-4o")

    @property
    def fallback_model(self) -> str:
        return os.environ.get("CLAW_FALLBACK_MODEL", "gpt-4o")
    
    @property
    def chroma_db_path(self) -> str:
        return os.environ.get("CLAW_CHROMA_DB_PATH", "./.chroma")

    @property
    def api_base(self) -> str:
        # Defaulting to OpenAI compatible URL.
        return os.environ.get("CLAW_API_BASE", "https://api.openai.com/v1")

    @property
    def api_key(self) -> str:
        return os.environ.get("CLAW_API_KEY", os.environ.get("OPENAI_API_KEY", ""))

config = Config()

import os


class Config:
    """Configuration class to manage environment variables."""
    LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "http://localhost:11434")
    LLM_NAME = os.getenv("LLM_NAME", "gpt-oss:20b")
    LLM_APIKEY = os.getenv("LLM_APIKEY", "**FakeKEy**")

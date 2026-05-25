
    
from pathlib import Path


class Settings:

    TOOL_CALLING_MODEL = (
        "qwen/qwen3-32b"
    )

    FALLBACK_TOOL_MODELS = [

        "llama-3.3-70b-versatile",

        "deepseek-r1-distill-llama-70b"
    ]

    REASONING_MODEL = (
        "qwen/qwen3-32b"
    )

    FALLBACK_REASONING_MODELS = [

        "deepseek-r1-distill-llama-70b",

        "llama-3.3-70b-versatile"
    ]

    EMBEDDING_MODEL = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    TEMPERATURE = 0

    BASE_DIR = (
        Path(__file__).resolve().parent.parent
    )

    VECTOR_DB_DIR = (
        BASE_DIR / "vector_db"
    )

    UPLOAD_DIR = (
        BASE_DIR / "uploaded_files"
    )

    VISUALIZATION_DIR = (
        BASE_DIR / "visualizations"
    )

    REPORT_DIR = (
        BASE_DIR / "reports"
    )
    COPILOT_MODEL = (
        "llama-3.1-8b-instant"
    )
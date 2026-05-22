from pathlib import Path

class Settings:

    TOOL_CALLING_MODEL = (
        "qwen/qwen3-32b"
    )

    REASONING_MODEL = (
        "qwen/qwen3-32b"
    )
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
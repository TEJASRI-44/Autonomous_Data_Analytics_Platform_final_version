# utils/llm_utils.py
import re

def clean_llm_output(text: str) -> str:
    """
    Removes <think>...</think> tags and all content inside them 
    from raw LLM response strings.
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Matches <think> blocks across multiple lines (re.DOTALL) and strips them
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

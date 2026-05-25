import re


def clean_llm_output(text):

    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL
    )

    if "<think>" in text:

        text = text.split(
            "<think>"
        )[0]

    return text.strip()
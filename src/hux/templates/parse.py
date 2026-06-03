import re

CODE_PATTERN = r"```+[ \t]*(.*?)[ \t]*\n(.*?)```+"


def extract_code(pattern: str, text: str) -> tuple[str, str]:
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        if "`" in match.group(2):
            return match.group(1), "tried codeblock escaping"
        return match.group(1), match.group(2)
    return "Language unmatched", "No code"

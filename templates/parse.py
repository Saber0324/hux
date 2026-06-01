import re

PATTERN_PY = r"```+[ \t]*(py|python)[ \t]*\n(.*?)```+"
PATTERN_GO = r"```+[ \t]*(go|golang)[ \t]*\n(.*?)```+"
PATTERN_RS = r"```+[ \t]*(rs|rust)[ \t]*\n(.*?)```+"
PATTERN_BF = r"```+[ \t]*(bf|brainfuck)[ \t]*\n(.*?)```+"
PATTERN_C = r"```+[ \t]*(c)[ \t]*\n(.*?)```+"
PATTERN_CPP = r"```+[ \t]*(cpp|c\+\+)[ \t]*\n(.*?)```+"


def extract_code(pattern: str, text: str) -> tuple[str, str] | None:
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1), match.group(2)
    return None

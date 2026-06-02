from dataclasses import dataclass
import string


@dataclass
class Snippet:
    title: str
    description: str
    author_id: int
    locked: bool


@dataclass
class Warn:
    user_id: int
    reason: str
    moderator_id: int
    date: str
    warn_id: int


def parse_time(message: str):
    separated = [char for char in message]
    for_time = ""
    metric_time = ""

    for char in separated:
        if char in string.digits:
            for_time += char
        else:
            metric_time += char

    if metric_time.lower().strip().startswith("d"):
        metric_time = "days"
    elif metric_time.lower().strip().startswith("h"):
        metric_time = "hours"
    elif metric_time.lower().strip().startswith("m"):
        metric_time = "minutes"

    parsed_time = {metric_time: int(for_time)}

    return parsed_time

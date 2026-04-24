from dataclasses import dataclass


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

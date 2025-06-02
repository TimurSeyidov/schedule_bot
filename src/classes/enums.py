from enum import Enum
from dataclasses import dataclass


class SubscriptionType(Enum):
    """Типы подписки"""
    GROUP = "group"
    TEACHER = "teacher"


@dataclass
class Subscribe:
    id: int
    outer_id: int
    name: str | None
    user_id: str
    type: SubscriptionType

@dataclass
class Group:
    id: int
    name: str
    year: int

@dataclass
class Schedule:
    id: int
    group_id: int
    date: str
    position: int
    name: str
    description: str


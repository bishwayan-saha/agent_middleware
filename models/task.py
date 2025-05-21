from datetime import datetime
from typing import Any, List, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class TextPart(BaseModel):
    type: Literal["text"] = "text"
    text: str


Part = TextPart


class Message(BaseModel):
    role: Literal["user", "agent"]
    parts: List[Part]


class TaskStatus(BaseModel):
    state: str
    timestamp: datetime = Field(default_factory=datetime.now)


class Task(BaseModel):
    id: str
    status: TaskStatus
    history: List[Message]


class TaskSendParams(BaseModel):
    id: str
    session_id: str = Field(default_factory=lambda: uuid4().hex)
    message: Message
    historyLength: int | None = None
    metadata: dict[str, Any] | None = None

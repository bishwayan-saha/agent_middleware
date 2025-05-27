from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class StatusMessage(str, Enum):
    OK = "ok"
    ERROR = "error"


## General response structure
class ServerResponse(BaseModel):
    data: Any = Field(
        ...,
        description="Server response, can be list, dictionary or primitive data types",
    )
    status: StatusMessage = Field(..., description="HTTP response status message")
    message: str = Field(
        ..., description="general message representing server response"
    )
    timestamp: str = Field(
        default=datetime.now().__str__(), description="current timestamp for tracking"
    )


class Message(BaseModel):
    query: str = Field(..., description="User query to host agent")


class AgentDetails(BaseModel):
    agent_name: str = Field(..., description="name of the remote agent")
    url: str = Field(..., description="URL of agent server")


class InteropAEException(Exception):

    def __init__(self, message: str, status_code: int) -> None:
        self.message = message
        self.status_code = status_code

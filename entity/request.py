from pydantic import BaseModel, Field


class Message(BaseModel):
    query: str = Field(..., description="User query to host agent")


class AgentDetails(BaseModel):
    agent_name: str = Field(..., description="name of the remote agent")
    url: str = Field(..., description="URL of agent server")

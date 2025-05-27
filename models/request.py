from typing import Literal

from models.json_rpc import JSONRPCRequest, JSONRPCResponse
from models.task import Task, TaskSendParams


class SendTaskRequest(JSONRPCRequest):
    method: Literal["tasks/send"] = "tasks/send"
    params: TaskSendParams


class SendTaskResponse(JSONRPCResponse):
    result: Task | None = None
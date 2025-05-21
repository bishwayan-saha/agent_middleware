import logging
from uuid import uuid4

import httpx
from sqlalchemy.orm import Session

from client.client import A2AClient
from entity.db_models import Remote_Agent_Details_Master
from entity.request import AgentDetails, Message
from models.task import Task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def save_agent_card(agentDetails: AgentDetails, db: Session):
    async with httpx.AsyncClient() as client:
        well_known_url = f"{agentDetails.url.rstrip("/")}/.well-known/agent.json"
        response = await client.get(well_known_url)
        response.raise_for_status()
        logger.info("--- Agent Card retrieved from the server URL ---")
        remote_agent_details = Remote_Agent_Details_Master(
            agent_name=agentDetails.agent_name,
            server_url=agentDetails.url,
            agent_details=str(response.json()),
            created_by="bishwayan.saha@pwc.com",  ## hardcoded for now. Will be replaced when auth will be implemented
        )
        try:
            db.add(remote_agent_details)
            db.commit()
            db.refresh(remote_agent_details)
            logger.info("--- Remote agent details saved in the database ---")
            return {
                "message": "Agent added successfully!",
                "agent_id": str(remote_agent_details.agent_id),
                "agent_name": remote_agent_details.agent_name,
                "server_url": remote_agent_details.server_url,
                "agent_card": response.json(),
            }
        except Exception as e:
            db.rollback()
            return {"error": f"Failed to add agent, reason: {str(e)}"}


async def get_agent_response(message: Message, client: A2AClient, session_id: str):
    payload = {
        "id": uuid4().hex,
        "sessionId": session_id,
        "message": {"role": "user", "parts": [{"type": "text", "text": message.query}]},
    }
    try:
        task: Task = await client.send_task(payload)
        if task.history and len(task.history) > 1:
            reply = task.history[-1]
            return {"message": reply.parts[0].text}
        else:
            return {"message": "No response"}
    except Exception as e:
        logger.error(
            f"An error occurred while fetching respons from agent\n reason: {e}"
        )
        return {"message": "Some error occurred"}

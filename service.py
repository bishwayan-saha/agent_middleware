import logging
from uuid import uuid4

import httpx
from client.client import A2AClient
from models.task import Task
from fastapi import status
from sqlalchemy.orm import Session

from entity.db_models import Remote_Agent_Details_Master, Credentials_Master
from entity.request import AgentDetails, InteropAEException, Message, CredentialDetails

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
                "agent_id": str(remote_agent_details.agent_id),
                "agent_name": remote_agent_details.agent_name,
                "server_url": remote_agent_details.server_url,
                "agent_card": response.json(),
            }
        except Exception as e:
            db.rollback()
            logger.error(f"Erorr occurred while saving agent details\n reason: {str(e)}")
            raise InteropAEException(
                message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


async def get_agent_response(message: Message, client: A2AClient, session_id: str):
    payload = {
        "id": uuid4().hex,
        "session_id": session_id,
        "message": {"role": "user", "parts": [{"type": "text", "text": message.query}]},
    }
    try:
        task: Task = await client.send_task(payload)
        if task.history and len(task.history) > 1:
            reply = task.history[-1]
            return reply.parts[0].text
        else:
            return "No response"
    except Exception as e:
        logger.error(
            f"An error occurred while fetching respons from agent\n reason: {e.__str__()}"
        )
        raise InteropAEException(
            message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

async def save_new_credential(credential_details_dto: CredentialDetails, db: Session) -> str:
    try:
        credential_details: Credentials_Master = Credentials_Master(
                credential_name=credential_details_dto.credential_name,
                credential_value=credential_details_dto.credential_value,
                created_by="bishwayan.saha@pwc.com"
        )
        db.add(credential_details)
        db.commit()
        db.refresh(credential_details)
        logger.info("--- New credential details saved in the database ---")
        return "credential added successfully"
    except Exception as e:
        db.rollback()
        logger.error(f"Erorr occurred while adding credential details\n reason: {str(e)}")
        raise InteropAEException(
            message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

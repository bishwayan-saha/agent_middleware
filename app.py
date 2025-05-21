import logging
from contextlib import asynccontextmanager
from typing import List
from uuid import uuid4

from fastapi import Depends, FastAPI, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from client.client import A2AClient
from database import SessionLocal
from entity.db_models import Credentials_Master, Remote_Agent_Details_Master
from entity.request import AgentDetails, Message
from service import get_agent_response, save_agent_card

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db: Session = SessionLocal()
    try:
        credentials: List[Credentials_Master] = db.query(Credentials_Master).all()
        logger.info("Credentials table loaded from DB")
        app.state.credentials = {}
        for credential in credentials:
            app.state.credentials[credential.credential_name] = (
                credential.credential_value
            )

        remote_agents: List[Remote_Agent_Details_Master] = db.query(
            Remote_Agent_Details_Master
        ).all()
        logger.info("Remote Agents table loaded from DB")
        app.state.agent_cards = [agent.agent_details for agent in remote_agents]

        yield
    finally:
        db.close()


app = FastAPI(lifespan=lifespan)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


client = A2AClient(url="http://localhost:10000")

session_id = uuid4().hex


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        db_status = "unreachable"

    return {
        "status": "ok",
        "message": "Server is running",
        "database": db_status,
    }


@app.get("/credentials")
def get_credentials():
    return JSONResponse(content={"message": app.state.credentials})


@app.get("/agent_cards", status_code=status.HTTP_200_OK)
def get_agent_cards():
    return JSONResponse(content={"message": app.state.agent_cards})


@app.post("/response", status_code=status.HTTP_200_OK)
async def get_response(message: Message):
    response = await get_agent_response(message, client, session_id)
    return JSONResponse(content=response)


@app.post("/register_agent", status_code=status.HTTP_201_CREATED)
async def register_agent(agentDetails: AgentDetails, db: Session = Depends(get_db)):
    response = await save_agent_card(agentDetails=agentDetails, db=db)
    return JSONResponse(content=response)

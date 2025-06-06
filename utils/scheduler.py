import logging

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session

from database import SessionLocal
from entity.db_models import Remote_Agent_Details_Master

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_agents_status():
    db: Session = SessionLocal()
    try:
        remote_agents = db.query(Remote_Agent_Details_Master).all()
        updated_remote_agents: list[Remote_Agent_Details_Master] = []
        for agent in remote_agents:
            try:
                url = agent.server_url.rstrip("/") + "/.well-known/agent.json"
                res = requests.get(url, timeout=5)
                agent_new_status = "ONLINE" if res.status_code == 200 else "OFFLINE"
            except Exception as e:
                logger.error(
                    f"Error occurred while fetching {agent.agent_name} status.\n Reason: {e}"
                )
                agent_new_status = "OFFLINE"
            if agent.agent_status != agent_new_status:
                agent.agent_status = agent_new_status
                updated_remote_agents.append(agent)
        if updated_remote_agents:
            logger.info(
                f"Status of these agents [{", ".join([agent.agent_name for agent in updated_remote_agents])}] changed."
            )
            db.add_all(updated_remote_agents)
        db.commit()
    except Exception as e:
        logger.error(f"Error during agent status check. \n Reason {e}")
    finally:
        db.close()


# APScheduler setup
scheduler = BackgroundScheduler()
scheduler.add_job(check_agents_status, CronTrigger(minute="*/1"))

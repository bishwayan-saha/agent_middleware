import requests
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from entity.db_models import Remote_Agent_Details_Master
from .database import SessionLocal

def check_agents_status():
    db: Session = SessionLocal()
    try:
        agents = db.query(Remote_Agent_Details_Master).all()
        for agent in agents:
            try:
                url = agent.server_url.rstrip('/') + "/.well-known/agent.json"
                res = requests.get(url, timeout=5)
                agent.status = "online" if res.status_code == 200 else "offline"
            except Exception:
                agent.status = "offline"
        db.commit()
    except Exception as e:
        print("Error during agent status check:", e)
    finally:
        db.close()


# APScheduler setup
scheduler = BackgroundScheduler()
scheduler.add_job(check_agents_status, CronTrigger(minute="*/15"))
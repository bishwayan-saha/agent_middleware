from sqlalchemy import DATETIME, Column, String, Text
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Credentials_Master(Base):

    __tablename__ = "credentials_master"

    credential_id = Column(
        name="credential_id",
        type_=UNIQUEIDENTIFIER,
        primary_key=True,
        server_default="NEWID()",
    )
    credential_name = Column(name="credential_name", type_=String, nullable=False)
    credential_value = Column(name="credential_value", type_=Text, nullable=False)
    created_by = Column(name="created_by", type_=String, nullable=False)
    created_at = Column(name="created_at", type_=DATETIME, nullable=False)
    updated_by = Column(name="updated_by", type_=String, nullable=True)
    updated_at = Column(name="updated_at", type_=DATETIME, nullable=True)

    def __str__(self):
        return (
            f"Credentials_Master("
            f"credential_id={self.credential_id}, "
            f"credential_name={self.credential_name}, "
            f"credential_value={self.credential_value}, "
            f"created_by={self.created_by}, "
            f"created_at={self.created_at}, "
            f"updated_by={self.updated_by}, "
            f"updated_at={self.updated_at})"
        )


class Remote_Agent_Details_Master(Base):

    __tablename__ = "remote_agent_details_master"

    agent_id = Column(
        name="agent_id",
        type_=UNIQUEIDENTIFIER,
        primary_key=True,
        server_default="NEWID()",
    )
    agent_name = Column(name="agent_name", type_=String, nullable=False)
    server_url = Column(name="server_url", type_=String, nullable=False)
    agent_details = Column(name="agent_details", type_=Text, nullable=False)
    created_by = Column(name="created_by", type_=String, nullable=False)
    created_at = Column(
        name="created_at", type_=DATETIME, nullable=False, server_default="GETDATE()"
    )
    updated_by = Column(name="updated_by", type_=String, nullable=True)
    updated_at = Column(name="updated_at", type_=DATETIME, nullable=True)

    def __init__(
        self,
        agent_name,
        server_url,
        agent_details,
        created_by,
        updated_by=None,
        updated_at=None,
    ):
        self.agent_name = agent_name
        self.server_url = server_url
        self.agent_details = agent_details
        self.created_by = created_by
        self.updated_by = updated_by
        self.updated_at = updated_at

    def __str__(self):
        return f"""Remote_Agent_Details_Master(agent_name={self.agent_name}, 
                    server_url={self.server_url}, created_by={self.created_by}, 
                    created_at={self.created_at}, updated_by={self.updated_by}, updated_at={self.updated_at})"""

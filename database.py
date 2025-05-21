from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = URL.create(
    drivername="mssql+pyodbc",
    username="interopae_dev",
    password="User@PwCAdmin",
    host="tcp:interopae-dev1.database.windows.net",
    database="Interop_AE",
    query={"driver": "ODBC Driver 17 for SQL Server"},
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

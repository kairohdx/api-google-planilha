import os
import os.path
from multiprocessing import connection
from typing import Any

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings

class Settings:
    _cors:list[str] = []
    secret_key:str = 'secret_key'
    app_name: str = 'API-IN-FASTAPI'
    admin_email:str = "kairohdx.faria@gmail.com"
    dbConn:str | None = None
    dbViewConn:str | None = None
    dbUser:str | None = None
    dbPass:str | None = None
    dbCli: Any
    db:Any

    def __init__(self) -> None:
        self._load_env()
        self.load_db_conn()

    def _load_env(self) -> None:
        if os.getenv('AMBIENTE') != 'PRD':
            load_dotenv()

        self.app_name = os.getenv('APP_NAME') if os.getenv('APP_NAME') else 'API-IN-FASTAPI'
        
        self._cors.append(os.getenv('CORS').split(";"))
        self.secret_key = os.getenv('SECRET_KEY')

        self.dbUser = os.getenv('MONGODB_USER')
        self.dbPass = os.getenv('MONGODB_PASS')
        self.dbConn = f"mongodb+srv://{self.dbUser}:{self.dbPass}@clusterpocketsb.yw1fh.mongodb.net/?retryWrites=true&w=majority"
        self.dbViewConn = f"mongodb+srv://<userName>:<password>@clusterpocketsb.yw1fh.mongodb.net/?retryWrites=true&w=majority"


    def load_db_conn(self):
        self.dbCli = AsyncIOMotorClient(self.dbConn)
        self.db = self.dbCli["db-forms"] #Nome do DataBase no cluster do mongo.

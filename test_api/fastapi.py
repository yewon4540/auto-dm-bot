from fastapi import FastAPI, Request
from dotenv import load_dotenv
import subprocess
import pymysql
import os

load_dotenv()

app = FastAPI()

# MariaDB 연결 설정
db_config = {
    "host"='localhost',
    "port"=int(os.getenv('MARIADB_PORT')),
    "user"=os.getenv('MARIADB_USER'),
    "password"=os.getenv('MARIADB_PW'),
    "database"=os.getenv('MARIADB_NAME')
}

@app.post("/events")
async def handle_event(request: Request):
    """MariaDB 트리거에서 전달된 이벤트 처리"""
    data = await request.json()
    event_type = data.get("event_type")
    reference_id = data.get("reference_id")

    if event_type == "INSERT":
        subprocess.run(["python3", "process_event.py", str(reference_id)])
    return {"status": "success", "event": data}

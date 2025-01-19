from fastapi import FastAPI, Request, Query, HTTPException
from dotenv import load_dotenv
from slack_utils import *
import subprocess
import pymysql
import os
# uvicorn api_server:app --host 0.0.0.0 --port 8000

# load_dotenv('/home/ubuntu/slack_dm')
load_dotenv()
print(int(os.getenv('MARIADB_PORT')))
print(os.getenv('MARIADB_USER'))
app = FastAPI()

# MariaDB 연결 설정
db_config = {
    "host":'localhost',
    "port":int(os.getenv('MARIADB_PORT')),
    "user":os.getenv('MARIADB_USER'),
    "password":os.getenv('MARIADB_PW'),
    "database":os.getenv('MARIADB_NAME')
}

# 테스트용
user_id = YEWON = os.getenv('YEWON')
text = '트리거 테스트'
c3_text = '전체 공지사항에 글이 추가되었습니다.'
c2_text = '그짝 게시판에 글이 추가되었습니다.'
channel_id = CHANNEL = os.getenv('CHANNEL')
cno = '채널'



@app.post("/events")
async def handle_event(
    event_type: str = Query(..., description="이벤트 타입"),
    reference_id: int = Query(None, description="참조 ID"),
    # cno: int = Query(None, description="클래스 번호 (CNO)"),
    no: int = Query(None, description="출결 고유 번호"),
    student_name: str = Query(None, description="학생 이름"),
    morning_check: str = Query(None, description="아침 체크 상태"),
    lunch_check: str = Query(None, description="점심 체크 상태"),
    afternoon_check: str = Query(None, description="오후 체크 상태")
):
    """MariaDB 트리거에서 전달된 이벤트 처리"""
    try:
        # event_type에 따라 동작 분기
        if event_type == "INS01":
            # send_dm 호출
            result = send_dm(user_id, text) # user_id, text 임의값
            return {
                "status": "success",
                "event_type": event_type,
                "reference_id": reference_id,
                "message": "DM sent successfully",
                "result": result
            }
            
        elif event_type == "INS02":
            # INS02: 클래스룸 게시판 이벤트 처리
            message = f"클래스룸 게시판(CNO={cno})에 새로운 글이 추가되었습니다. Reference ID: {reference_id}" # cno(게시판 구별번호) 임의 값
            send_channel_message(channel_id, message) # channel_id, text 임의값
            return {
                "status": "success",
                "event_type": event_type,
                "reference_id": reference_id,
                # "cno": cno,
                "message": "Classroom board event processed"
            }
            
        elif event_type == "INS03":
            # INS03: 전체 공지사항 이벤트 처리
            message = f"전체 공지사항(CNO={cno})에 새로운 글이 추가되었습니다. Reference ID: {reference_id}"
            send_channel_message(channel_id, message) # channel_id, text 임의값
            return {
                "status": "success",
                "event_type": event_type,
                "reference_id": reference_id,
                # "cno": cno,
                "message": "Global notice event processed"
            }
            
        elif event_type == "INS04":
            # 출결 상태 지연 이벤트 처리
            message = "님 지각임 ㅋ"
            # user_id = 
            # message = f""
            send_dm(user_id, message)
            return {
                "status": "success",
                "event_type": event_type,
                # "no": no,
                # "student_name": student_name,
                # "morning_check": morning_check,
                # "lunch_check": lunch_check,
                # "afternoon_check": afternoon_check,
                # "message": "Attendance delay event processed"
            }
            
        else:
            # 처리되지 않는 이벤트 타입에 대한 오류 반환
            raise HTTPException(status_code=400, detail="Unsupported event_type")
    except Exception as e:
        return {"status": "error", "message": str(e)}





# # json 타입 버전
# async def handle_event(request: Request):
#     """MariaDB 트리거에서 전달된 이벤트 처리"""
#     try:
#         data = await request.json()
#         event_type = data.get("event_type")
#         reference_id = data.get("reference_id")

#         if event_type == "INSERT" and reference_id:
#             # 이벤트를 처리하는 외부 Python 스크립트 호출
#             subprocess.run(["python3", "process_event.py", str(reference_id)])
#             return {"status": "success", "event": data}
#         else:
#             return {"status": "error", "message": "Invalid event data"}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

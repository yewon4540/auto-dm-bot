import os
import discord
import pymysql
import time
from dotenv import load_dotenv

load_dotenv()

# Discord 봇 설정
TOKEN = os.getenv('TOKEN')
intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents=intents)

# DB 연결 설정
db = pymysql.connect(
    host='localhost',
    port=int(os.getenv('MARIADB_PORT')),
    user=os.getenv('MARIADB_USER'),
    password=os.getenv('MARIADB_PW'),
    database=os.getenv('MARIADB_NAME')
)

async def process_and_send_dm():
    while True:
        try:
            cursor = db.cursor()
            # is_processed가 0인 데이터 가져오기
            query = """
                SELECT student_no, discord_id, morning_reason
                FROM attend_dm
                WHERE is_processed = 0
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                student_no, discord_id, morning_reason = row

                try:
                    # Discord 사용자 가져오기
                    user = await bot.fetch_user(discord_id)

                    # DM 발송
                    message = f"{student_no}님, '{morning_reason}'으로 기록되었습니다. 다음부터는 시간을 준수해주세요!"
                    if user.dm_channel is None:
                        await user.create_dm()
                    await user.send(message)

                    # DM 발송 성공 시 is_processed 업데이트
                    update_query = "UPDATE attend_dm SET is_processed = 1 WHERE student_no = %s"
                    cursor.execute(update_query, (student_no,))
                    db.commit()
                    print(f"{student_no}에게 DM 발송 성공.")
                except discord.errors.Forbidden:
                    # DM 발송 실패 시 처리
                    print(f"{student_no}에게 DM 발송 실패. Discord 설정을 확인하세요.")
                    update_query = "UPDATE attend_dm SET is_processed = -1 WHERE student_no = %s"
                    cursor.execute(update_query, (student_no,))
                    db.commit()
                except Exception as e:
                    print(f"{student_no} 처리 중 오류 발생: {e}")
        except Exception as e:
            print(f"데이터베이스 처리 중 오류 발생: {e}")
        finally:
            time.sleep(10)  # 10초마다 확인

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await process_and_send_dm()  # DM 발송 프로세스 시작

bot.run(TOKEN)


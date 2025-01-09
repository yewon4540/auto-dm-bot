import os
import discord
import pymysql
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
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def send_late_dm(student_id):
    cursor = db.cursor()
    # 학생 출석 상태와 디스코드 ID 조회
    query = f"SELECT discord_id FROM students WHERE student_id = '{student_id}' AND attendance_status = 'late'"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        discord_id = result[0]
        user = await bot.fetch_user(discord_id)
        message = "수업에 지각하셨습니다. 다음부터는 정시에 참여해주세요!"
        await user.send(message)
        print(f'{user}에게 DM을 보냈습니다.')

# 수동 테스트
@bot.event
async def on_message(message):
    if message.content.startswith("!지각"):
        student_id = message.content.split(" ")[1]
        await send_late_dm(student_id)

bot.run(TOKEN)

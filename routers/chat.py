from google import genai
from os import getenv
from dotenv import load_dotenv 

# 1. .env 로드, DB URL 확보
load_dotenv(".env", override = True) #BASE_DIR에 저장된 .env 파일을 로드함. 기존 환경 변수와 이름이 겹칠 경우 덮어씀 (Override = True)



client = genai.Client(api_key=getenv('GEMINI_API_KEY')) #API 키를 가져온다
chat = client.aio.chats.create(model="gemini-2.5-flash", config=None)
# config = system_instruction 해 두고 여기 config = {} ->dictionary 만들어서
#  prompt를 작성한다

# chat.sendmassage()

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def send_chat():
    res = await chat.send_message("What are some of the beautiful things in life?")
    
    return {"response" : res.text}




#front에서 특정 주소로 요청을 하고, 요청이 오면 todo


    #여러 사용자가 활용하는 경우 -> 사용자마자 create 해야 한다.
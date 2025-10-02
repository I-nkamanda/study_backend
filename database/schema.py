import os #os 모듈 불러옴. os.getenv (환경변수 읽어오기) 때문에 import 하게 됨
from pathlib import Path #file 시스템 경로를 객체지향적으로 다루기 위해서 (.env 파일 읽어오기 등) 사용함
import datetime as dt # created_at 필드에 사용됨 (타임스탬프 찍기)
from contextlib import asynccontextmanager #asynccontextmanager라는 데코레이터(비동기 컨텍스트 매니저 생성에 사용)를 불러옴. FastAPI의 lifespan 이벤트를 다루는 데 사용.

from fastapi import FastAPI, HTTPException # FastAPI: 웹 애플리케이션의 핵심 클래스 / HTTPException: HTTP 오류 응답을 반환함
from pydantic import BaseModel, EmailStr # BaseModel: 데이터 유효성 검사 / 설정 관리를 위한 기본 플래스, EmailStr: 이메일 형식의 문자열을 검증하는 데 사용됨
from dotenv import load_dotenv # .env 파일에 정의된 환경 변소를 현재 환경으로 로드하는데 사용됨
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import String, text, select # String: VARCHAR와 같은 문자열 데이터 타입, text: 원시 SQL 표현식, select: SELECT 쿼리 구성에 사용됨
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker #불러오는 각 구성요소들은 ORM (Object Relational Mapper)를 사용, 파이썬 클래스를 DB 테이블에 매핑하는 핵심 구성 요소
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession #SQLAlchemy를 비동기 환경에서 사용할 수 있게 해주는 클래스
import routers.chat as chat

from model.base import Base

BASE_DIR = Path(__file__).resolve().parent # 현재 파일의 경로 (__file__)을 가져와서 절대 경로로 변환 (.resolve())한 뒤, 부모 directory를 BASE_DIR 값으로 할당함. (루트 디렉토리 설정)

# 1. .env 로드, DB URL 확보
load_dotenv(".env", override = True) #BASE_DIR에 저장된 .env 파일을 로드함. 기존 환경 변수와 이름이 겹칠 경우 덮어씀 (Override = True)



DATABASE_URL = os.getenv("ASYNC_DATABASE_URL") #ASYNC_DATABASE_URL값을 가져와서 DATABASE_URL 에 저장
if not DATABASE_URL: #DATABASE_URL이 없을 경우에는
    raise RuntimeError("ASYNC_DATABASE_URL not set. Put it in a .env at project root.") #Runtime Error 예외를 발생시키고 "환경 변수가 설정되지 않았다. 루트 폴더에 넣어라"고 알림

# 2. SQLALCHEMY 비동기(async) 엔진/세션 DATABASE_URL:연결할 데이터베이스의 URL / echo=True: 실행되는 모든 SQL query를 터미널에 출력 (디버깅용) #pool_pre_ping -> 커넥션 풀 유효성 주기적으로 확인 여부 / connect_args = {"ssl":False} : 연결 시 SSL을 사용하지 않도록 설정함
engine = create_async_engine(DATABASE_URL, echo = True, pool_pre_ping=True, connect_args = {"ssl": False}) #비동기 데이터베이스 엔진을 생성. 
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit = False) #데이터베이스 세션을 생성하는 세션 팩토리(sessionmaker) 정의
 # bind = engine: 생성된 세션이 위에서 정의한 엔진과 연결되도록 함 #class_=AsyncSession: 비동기 세션 클래스를 사용하도록 지정 #expire_on_commit=False: 커밋 후에 객체 상태가 만료되지 않도록 설정함.



# 4. 서버 라이프사이클: 시작 시 테이블 자동 생성

@asynccontextmanager # 이 데코레이터는 비동기 컨텍스트 매니저를 생성함
async def lifespan(app:FastAPI): #FastAPI 애플리케이션의 시작 및 종료 시 이벤트를 처리하는 비동기 함수를 정의함
    async with engine.begin() as conn: #conn = await engine.conect() -> DB 엔진의 비동기 트랜잭션 블록을 시작. 이 블록은 DB 커넥션을 얻고, transaction을 시작하며, block 종료 시 자용으로 커밋 또는 rollback을 할 것임.
        await conn.run_sync(Base.metadata.create_all) # 없는 테이블만 생성 -> 커넥션(conn을 사용, 동기 함수인 Base.metadata.create_all)을 비동기적으로 실행. 아직 존재하지 않는 테이블만 데이터베이스에 생성 예정
    yield #이 지점에서 애플리케이션이 시작, 요청을 처리할 준비가 됨
    await engine.dispose() # 애플리케이션 종료 시 모든 데이터베이스 연결을 닫고 풀을 비움

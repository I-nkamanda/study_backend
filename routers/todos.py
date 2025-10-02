from fastapi import APIRouter


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
from model.todo import Todo
from database.schema import AsyncSessionLocal


router = APIRouter()


# 5. (테스트용) 간단 CRUD
class UserCreate(BaseModel): #Pydantic의 BaseModel을 상속받아 사용자 생성 요청 데이터의 유효성을 검사하는 schema를 정의함
    email: EmailStr #이메일 필드 정의, EmailStr 타입을 사용해서 형식이 이메일 형식인지 자동 유효성 검사

class TodoCreate(BaseModel):
    task: str
    is_important: int # bool -> int 로 수정함

@router.post("/")
async def create_todo(payload: TodoCreate):
    async with AsyncSessionLocal() as session: #Pydantic 모델의 bool을 DB에 저장할 int로 변환
        # is_important_int = 1 if payload.is_important else 0
        t = Todo(task=payload.task, is_important=payload.is_important) #바로 정수값을 받습니다.

        session.add(t)
        await session.commit()
        await session.refresh(t)

        #is_important를 다시 bool로 변환해서 응답
        return {
            "id": t.id,
            "task": t.task,
            "is_important": bool(t.is_important), # 추후에 int 그대로
            "is_completed": t.is_completed,
            "created_at": t.created_at
        }

@router.get("/")
async def list_todos():
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Todo).order_by(Todo.id.desc())) #최신순으로 정렬
        todos = res.scalars().all()

        #응답 데이터를 JSON 형식으로 변환
        return [
            {
                "id": todo.id,
                "task": todo.task,
                "is_important": bool(todo.is_important),
                "is_completed": todo.is_completed,
                "created_at": todo.created_at
            } for todo in todos
        ]

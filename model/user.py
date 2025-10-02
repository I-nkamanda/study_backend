from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import String, text, select # String: VARCHAR와 같은 문자열 데이터 타입, text: 원시 SQL 표현식, select: SELECT 쿼리 구성에 사용됨
import datetime as dt # created_at 필드에 사용됨 (타임스탬프 찍기)
from .base import Base

class User(Base): #Base 클래스를 상속받아서 User 모델을 정의
    __tablename__ = "users" # 이 클래스가 매핑될 데이터베이스 테이블의 이름을 "users"로 명명하는 부분
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) #id 필드를 정의함. 데이터 타입은 int, 기본 키로 설정(primary_key=True)되었으며, 자동증가(autoincrement) 하도록 설정됨
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False) #email 필드를 정의 데이터 타입은 문자열(string(255))이고, 값이 고유(unique:True)하며, 인덱스가 생성되고(index=True), NULL값을 받지 않는다 (nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"), nullable=False) #created_at 필드를 정의함. 데이터 타입은 datetime이며, DB 서버에서 자동으로 현재 시간을 기본값으로 설정하도록 (server_default=text("CURRENT_TIMESTAMP")) 함.


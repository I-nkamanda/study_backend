from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import String, text, select # String: VARCHAR와 같은 문자열 데이터 타입, text: 원시 SQL 표현식, select: SELECT 쿼리 구성에 사용됨
import datetime as dt # created_at 필드에 사용됨 (타임스탬프 찍기)
from model.base import Base

class Todo(Base):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    task: Mapped[str] = mapped_column(String(255), nullable=False)
    is_important: Mapped[int] = mapped_column(nullable=False, default = 0)
    is_completed: Mapped[bool] = mapped_column(nullable=False, default=False) #다 하지 않은 게 default
    created_at: Mapped[dt.datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"), 
        nullable = False)

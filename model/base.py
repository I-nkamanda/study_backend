from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase): #SQLAlchemy ORM에서 클래스를 데이터베이스 테이블에 매핑하기 위한 기본 클래스의 정의. 모든 모델은 이 클래스를 상속받음.
    pass
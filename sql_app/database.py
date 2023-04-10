from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# Create a database URL for SQLAlchemy¶
#sqlite db를 사용할거고, 위 Url에 해당하는곳에 저장됨.

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
#엔진 설정하기. 
#create_engine은 컨넥션 풀을 생성한다. 컨넥션 풀이란 데이터베이스에 접속하는 객체를 일정 갯수만큼 만들어 놓고 돌려가며 사용하는 것을 말한다. (컨넥션 풀은 데이터 베이스에 접속하는 세션수를 제어하고, 또 세션 접속에 소요되는 시간을 줄이고자 하는 용도로 사용한다.)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#그리고 SessionLocal은 데이터베이스에 접속하기 위해 필요한 클래스이다.

Base = declarative_base()
# declarative_base 함수에 의해 반환된 Base 클래스는 조금 후에 알아볼 데이터베이스 모델을 구성할 때 사용되는 클래스이다.


#이 주석부분들은 현재 깊이 탐구할 필요는 없다.
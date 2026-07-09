from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Đường dẫn đến file SQLite
DATABASE_URL = "sqlite:///./app/db/database.db"

# Tạo Engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Tạo Session
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# Base cho các model kế thừa
Base = declarative_base()


def get_db():
    """
    Tạo một Session cho mỗi request và tự động đóng sau khi sử dụng.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database
DATABASE_URL = "sqlite:///./shop.db"

# Tạo engine kết nối database
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Tạo session để thao tác DB
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class cho models
Base = declarative_base()


# Dependency lấy DB session
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
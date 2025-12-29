from sqlalchemy import Column, String, DateTime
from datetime import datetime
from src.database import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"

    username = Column(String(50), primary_key=True, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(username={self.username})>"

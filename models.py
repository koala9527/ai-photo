from sqlalchemy import Column, Integer, String, DateTime
from config.database import Base
from datetime import datetime

class WechatCode(Base):
    __tablename__ = "wechat_code"

    id = Column(Integer, primary_key=True, index=True)
    openid = Column(String(50), nullable=True)
    code = Column(String(10), unique=True, nullable=True)
    status = Column(Integer, nullable=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    created_at = Column(DateTime, default=datetime.now) 
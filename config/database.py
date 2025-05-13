from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'jijiwaiwai123')
DB_HOST = os.getenv('DB_HOST', '175.178.177.10')
DB_PORT = os.getenv('DB_PORT', '37087')
DB_NAME = os.getenv('DB_NAME', 'hyperf')

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 创建数据库引擎，配置连接池
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,  # 连接池大小
    max_overflow=10,  # 超过pool_size后最多可以创建的连接数
    pool_timeout=30,  # 连接池获取连接的超时时间
    pool_recycle=1800,  # 连接在连接池中重用的时间限制，这里设置为30分钟
    pool_pre_ping=True  # 每次连接前ping一下数据库，确保连接可用
)

# 创建线程安全的会话工厂
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

Base = declarative_base()

class DatabaseSession:
    def __init__(self):
        self.session = Session()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

def get_db():
    """获取数据库会话的上下文管理器"""
    return DatabaseSession() 
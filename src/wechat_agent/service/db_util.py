import os.path
import src.wechat_agent.conf as constants
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, text, Text
from sqlalchemy.orm import declarative_base, sessionmaker

user_dir = os.path.join(os.path.expanduser('~'))
db_file_path = user_dir + "/wechat-agent/db"
os.makedirs(db_file_path, exist_ok=True)

Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True

    create_time = Column(TIMESTAMP, server_default=text("DATETIME(CURRENT_TIMESTAMP, '+8 hours')"))
    update_time = Column(TIMESTAMP, server_default=text("DATETIME(CURRENT_TIMESTAMP, '+8 hours')"),
                         onupdate=text("DATETIME(CURRENT_TIMESTAMP, '+8 hours')"))

    def to_dic(self):
        res = {}
        for column in self.__table__.columns:
            if column.name == 'create_time' or column.name == 'update_time':
                res[column.name] = getattr(self, column.name).strftime("%Y-%m-%d %H:%M:%S")
            else:
                res[column.name] = getattr(self, column.name)
        return res
    # def to_dic(self):
    #     return {
    #         column.name: getattr(self, column.name)
    #         for column in self.__table__.columns
    #     }


class SysInfo(BaseEntity):
    # 定义表名
    __tablename__ = 'sys_info'
    # 定义字段
    id = Column(Integer, primary_key=True)
    platform = Column(String(50))
    os_arch = Column(String(50))
    gpu_platform = Column(String(50))
    version = Column(String(255))
    username = Column(String(32), nullable=False)
    password = Column(String(32), nullable=False)
    email = Column(String(50), nullable=False)
    model_save_dir = Column(String(255), nullable=False)
    proxy_host = Column(String(255))
    proxy_port = Column(Integer)


class Agent(BaseEntity):
    __tablename__ = 'agent'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    rule = Column(Text(), nullable=False)


class AiRole(BaseEntity):
    __tablename__ = 'ai_role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    prompt = Column(String(500), nullable=False)


class SqliteSqlalchemy(object):
    def __init__(self):
        # 创建Sqlite连接引擎
        engine = create_engine(constants.db_url.format(user_dir), echo=True)
        # 创建表
        Base.metadata.create_all(engine, checkfirst=True)
        # 创建Sqlite的session连接对象
        self.session = sessionmaker(bind=engine)()

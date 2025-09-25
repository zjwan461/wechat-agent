import os.path
import wechat_agent.conf as constants
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, text, Text, Double
from sqlalchemy.orm import declarative_base, sessionmaker
from wechat_agent.SysEnum import AiType, AgentType, AgentStatus, ChatType, WechatVersion

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
    wechat_install_path = Column(String(255), nullable=False)
    wechat_version = Column(String(50), nullable=False, default=WechatVersion.V3.value)
    my_wechat_names = Column(String(500), nullable=False)


class Agent(BaseEntity):
    __tablename__ = 'agent'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    nickname = Column(String(255), nullable=False)
    chat_type = Column(String(50), nullable=False, default=ChatType.PRIVATE.value)
    type = Column(String(50), nullable=False, default=AgentType.SIMPLE.value)
    reply_group = Column(String(50))
    memory_size = Column(Integer, nullable=False, default=3)
    model_id = Column(Integer)
    ai_role_id = Column(Integer)
    status = Column(String(50), nullable=False, default=AgentStatus.STOPPED.value)


class AiRole(BaseEntity):
    __tablename__ = 'ai_role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    prompt = Column(Text(), nullable=False)


class Reply(BaseEntity):
    __tablename__ = 'reply'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text(), nullable=False)
    group = Column(String(50), nullable=False, default='default')


class Model(BaseEntity):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False, default=AiType.LLM.value)
    provider = Column(String(50), nullable=False)
    base_url = Column(String(150), nullable=False)
    api_key = Column(String(100))
    temperature = Column(Double(), nullable=False, default=0.7)
    max_tokens = Column(Integer, nullable=False, default=2048)
    top_k = Column(Integer(), default=30)
    top_p = Column(Double(), default=0.9)


class SqliteSqlalchemy(object):
    def __init__(self):
        # 创建Sqlite连接引擎
        engine = create_engine(constants.db_url.format(user_dir), echo=True)
        # 创建表
        Base.metadata.create_all(engine, checkfirst=True)
        # 创建Sqlite的session连接对象
        self.session = sessionmaker(bind=engine)()

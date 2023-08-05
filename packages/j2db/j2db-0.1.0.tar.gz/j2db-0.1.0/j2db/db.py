from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError, InternalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import contextlib
from loguru import logger
import typing
import os

BaseModel = declarative_base()


class BaseManager(object):
    def __init__(self, *_, **__):
        self.engine: typing.Optional[Engine] = None
        self.session_maker: typing.Optional[typing.Type] = None
        self.models: typing.Dict[str, BaseModel] = {}

    def heartbeat(self) -> bool:
        if (not self.engine) or (not self.session_maker):
            return False
        try:
            self.engine.execute('SELECT "HELLO"')
        except (OperationalError, InternalError) as e:
            logger.error(e)
            return False
        return True

    def build_connect_command(self):
        raise NotImplementedError

    def connect(self, *args, **kwargs):
        self.engine = create_engine(self.build_connect_command(), *args, **kwargs)
        self.session_maker = scoped_session(sessionmaker(bind=self.engine))
        assert self.heartbeat(), "connect failed"
        logger.info("connected")

    def add_model(self, model: BaseModel):
        table_name = model.__tablename__
        self.models[table_name] = model
        logger.info(f"model of {table_name} added")

    def remove_model(self, model: BaseModel):
        table_name = model.__tablename__
        del self.models[table_name]
        logger.info(f"model of {table_name} removed")

    def apply_action(self, action_name: str, *args, **kwargs) -> typing.Optional[str]:
        action_dict: typing.Dict[str, typing.Callable] = {
            "insert": self.insert,
            # NOTIMPLEMENTED
            # 'update': self.update,
            # FORBIDDEN
            # 'query': self.query,
            # 'remove': self.remove,
        }
        if (not action_name) or (action_name not in action_dict):
            error_msg = (
                f"action should be one of these options: {list(action_dict.keys())}"
            )
            logger.warning(error_msg)
            return error_msg
        return action_dict[action_name](*args, **kwargs) or ""

    # TODO maybe these events should be handled by queue?
    def insert(self, data, *_, **__) -> typing.Optional[Exception]:
        try:
            with session_scope(self.session_maker) as session:
                session.add(data)
                session.commit()
                session.flush()
        except Exception as e:
            logger.error(e)
            return e


class SQLiteManager(BaseManager):
    def __init__(self, path_to_db: str, *args, **kwargs):
        super(SQLiteManager, self).__init__(*args, **kwargs)
        assert os.path.isfile(path_to_db), f"db {path_to_db} not existed"
        self.path: str = path_to_db

    def build_connect_command(self):
        return f"sqlite:///{self.path}"


class MySQLManager(BaseManager):
    def __init__(
            self,
            url: str,
            port: int,
            user: str,
            password: str,
            db_name: str,
            *args,
            **kwargs,
    ):
        super(MySQLManager, self).__init__(*args, **kwargs)
        self.url: str = url
        self.port: int = port
        self.user: str = user
        self.password: str = password
        self.db_name: str = db_name

    def build_connect_command(self) -> str:
        return (
            f"mysql+pymysql://"
            f"{self.user}:{self.password}"
            f"@"
            f"{self.url}:{self.port}"
            f"/"
            f"{self.db_name}"
        )


@contextlib.contextmanager
def session_scope(maker: typing.Type):
    """Provide a transactional scope around a series of operations."""
    session = maker()
    try:
        yield session
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise e
    finally:
        session.close()

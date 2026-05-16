from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


load_dotenv() 

engine_master = create_engine(f"postgresql://{os.getenv('MASTER_USER')}:{os.getenv('MASTER_PASSWORD', "")}@"
f"{os.getenv('MASTER_HOST')}:{os.getenv('MASTER_PORT')}/{os.getenv('MASTER_NAME')}")  # URL для мастер

engine_replica = create_engine(f"postgresql://{os.getenv('REPLICA_USER')}:{os.getenv('REPLICA_PASSWORD')}@"
f"{os.getenv('REPLICA_HOST_REPLICA')}:{os.getenv('REPLICA_PORT')}/{os.getenv('REPLICA_NAME')}")  # URL для реплики

SessionLocalMaster = sessionmaker(bind=engine_master)  # фабрика сессий
SessionLocalReplica = sessionmaker(bind=engine_replica)  # фабрика сессий

@contextmanager
def get_session(read_only=False):
    if read_only:
        print("Читаю из реплики")
        session = SessionLocalReplica()
    else:
        print("Запись в master")
        session = SessionLocalMaster()
    try:
        yield session
        if not read_only:
            session.commit()
    except Exception as e:
        if not read_only:
            session.rollback()
        raise
    finally:
        session.close()

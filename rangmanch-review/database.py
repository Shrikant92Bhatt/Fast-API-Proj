from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "sqlite:///rangmanch.db"
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    '''Create all table defined by SQL models'''
    SQLModel.metadata.create_all(engine)

def get_session():
    '''Dependency that provide a database session per request'''
    with Session(engine) as session:
        yield session

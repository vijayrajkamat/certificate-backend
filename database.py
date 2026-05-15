from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///certificates.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class CertificateSubmission(Base):

    __tablename__ = "certificate_submissions"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, nullable=False)

    name = Column(String, nullable=False)

    strengths = Column(Text)

    skills = Column(Text)

    values = Column(Text)

    passions = Column(Text)

    purpose = Column(Text)


def init_db():

    Base.metadata.create_all(bind=engine)
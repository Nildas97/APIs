# OBJECT RELATIONAL MAPPER (ORM)
# Layer of abstraction that sits between the database and user.
# It performs all database operations using python code instead of SQL.

# HOW ORM WORKS
# instead of manually defining tables in postgres, we can define our tables as python models.
# queries can be made exclusively through python code.No SQL required.

# SQLALCHEMY
# it is the most popular standalone library python ORMs.

# importing libraries
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# connection string
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin123@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

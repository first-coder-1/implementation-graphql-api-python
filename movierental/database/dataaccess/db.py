import databases
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://admin:admin@localhost/pagila"

engine = create_engine("postgresql://admin:admin@localhost/pagila", echo=True)

Session = sessionmaker(bind=engine)
session = Session()

db = databases.Database(DATABASE_URL)

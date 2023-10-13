from hashlib import sha256

from config.config import ConfigClass
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from repositories.tables import UsersTable

import argparse

Base = declarative_base()

engine = create_engine(ConfigClass.SQL_CONNECTION_STRING)
Base.metadata.create_all(engine)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

parser = argparse.ArgumentParser(description="Procssing username and password")
parser.add_argument('username', type=str)
parser.add_argument("password", type=str)
parser.add_argument("role", help="1- admin, 2- normal user", type=str)
# parser.add_argument("delivery_center_id", type=str)
args = parser.parse_args()
username, password, role= args.username, args.password, args.role

password_cipher = sha256()
password_cipher.update(password.encode())
password_cipher.update(ConfigClass.PASSWORD_PEPPER.encode())
with Session() as session:
    try:
        new_record = UsersTable(
            username=username,
            password=password_cipher.hexdigest(),
            role=role
        )
        session.add(new_record)
        session.commit()
    except Exception as e:
        print(f"Exception: {e}")
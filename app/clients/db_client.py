from repositories.tables import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBclient():
    def __init__(self, connection: str):
        self.engine = create_engine(connection)
        Base.metadata.create_all(self.engine)

        self._Session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self._session = self._Session()

    def add(self, instance):
        self._session.add(instance)

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
        
    def query(self, instance):
        return self._session.query(instance)

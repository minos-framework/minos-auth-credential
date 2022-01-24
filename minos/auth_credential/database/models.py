import uuid

from sqlalchemy import (
    TIMESTAMP,
    Column,
    String,
)
from sqlalchemy.dialects.postgresql import (
    UUID,
)
from sqlalchemy.ext.declarative import (
    declarative_base,
)

Base = declarative_base()


class Credential(Base):
    __tablename__ = "credential"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String, primary_key=True, unique=True)
    password = Column(String)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return "<Credential(uuid='{}', username='{}', password={}, created_at={}, updated_at={})>".format(
            self.uuid, self.username, self.password, self.created_at, self.updated_at
        )

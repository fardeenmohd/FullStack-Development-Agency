from sqlalchemy import Column, UUID, JSONB, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Alert(Base):
    __tablename__ = 'alerts'
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, server_default=PGUUID(as_uuid=True).default)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    criteria = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP, default=TIMESTAMP().default)

    user = relationship("User", back_populates="alerts")

# Indexing
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:password@localhost/dbname')
Base.metadata.create_all(engine)

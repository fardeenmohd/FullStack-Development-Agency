from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UUID, TIMESTAMP, DECIMAL, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import uuid

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define models
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    country = Column(String(100), nullable=False)
    iec_code = Column(String(50), nullable=True)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())

class Product(Base):
    __tablename__ = "products"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    hs_code = Column(String(12), nullable=False)
    description = Column(Text, nullable=False)
    target_regions = Column(ARRAY(String), nullable=False)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())

class Lead(Base):
    __tablename__ = "leads"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    company_name = Column(String(255), nullable=False)
    country = Column(String(100), nullable=False)
    contact_email = Column(String(255), nullable=True)
    confidence_score = Column(DECIMAL(5, 2), nullable=False)
    source_url = Column(Text, nullable=True)
    status = Column(String(50), default='NEW', nullable=False)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"), nullable=False)
    exporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    contract_value = Column(DECIMAL(15, 2), nullable=False)
    currency = Column(String(3), default='USD', nullable=False)
    status = Column(String(50), default='INITIATED', nullable=False)
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

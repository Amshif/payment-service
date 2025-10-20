from sqlalchemy import Column, String, Boolean, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid
import enum

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"
    support = "support"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String(20))
    name = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, default={})

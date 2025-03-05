from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.models import Base
import uuid

class ProcessingSession(Base):
    __tablename__ = "processing_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))  # Unique request ID
    status = Column(String, default="processing")  # Processing status ("processing", "completed", "failed")

    # Relationship to ProductDetail
    products = relationship("ProductDetail", back_populates="session", cascade="all, delete")

    def as_dict(self):
        return {
            "id": self.id,
            "status": self.status
        }

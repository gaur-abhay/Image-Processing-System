from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.models import Base

class ProductDetail(Base):
    __tablename__ = "product_details"

    id = Column(String, primary_key=True)  # Unique ID: request_id + product_name
    request_id = Column(String, ForeignKey("processing_sessions.id"))  # Link to session
    serial_number = Column(String, nullable=False)
    product_name = Column(String)  # Stores product name
    input_urls = Column(Text)  # Comma-separated input image URLs
    output_urls = Column(Text, nullable=True)  # Comma-separated processed image URLs

    # Relationship to ProcessingSession
    session = relationship("ProcessingSession", back_populates="products")

    def __init__(self, request_id, serial_number, product_name, input_urls):
        self.request_id = request_id
        self.serial_number = serial_number
        self.product_name = product_name
        self.input_urls = input_urls

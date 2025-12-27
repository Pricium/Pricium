from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    base_price = Column(Float, nullable=False)
    unit = Column(String(50), default="unit")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    estimates = relationship("Estimate", back_populates="service")


class Material(Base):
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    multiplier = Column(Float, default=1.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    estimates = relationship("Estimate", back_populates="material")


class ComplexityLevel(Base):
    __tablename__ = "complexity_levels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    multiplier = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    estimates = relationship("Estimate", back_populates="complexity")


class Estimate(Base):
    __tablename__ = "estimates"
    
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=True)
    complexity_id = Column(Integer, ForeignKey("complexity_levels.id"), nullable=False)
    
    quantity = Column(Integer, nullable=False)
    length = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    
    base_price = Column(Float, nullable=False)
    complexity_multiplier = Column(Float, nullable=False)
    material_multiplier = Column(Float, default=1.0)
    quantity_multiplier = Column(Float, default=1.0)
    dimension_multiplier = Column(Float, default=1.0)
    
    total_price = Column(Float, nullable=False)
    
    client_name = Column(String(200), nullable=True)
    client_email = Column(String(200), nullable=True)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    service = relationship("Service", back_populates="estimates")
    material = relationship("Material", back_populates="estimates")
    complexity = relationship("ComplexityLevel", back_populates="estimates")


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

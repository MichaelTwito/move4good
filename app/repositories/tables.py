from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float

Base = declarative_base()

class UsersTable(Base):
    __tablename__ = 'users'
    username = Column(String(255), primary_key=True, index=True)
    password = Column(String(255))
    role = Column(String(255))
    delivery_center_id = Column(String(255), ForeignKey('delivery_centers.id'))
    delivery_center = relationship('DeliveryCenterTable', back_populates='users')

class DeliveryCenterTable(Base):
    __tablename__ = 'delivery_centers'
    id = Column(String(255), primary_key=True, index=True, default=0)
    lng = Column(Float)
    lat = Column(Float)
    orders = relationship('OrdersTable', back_populates='delivery_center')
    users = relationship('UsersTable', back_populates='delivery_center', uselist=False)

class OrdersTable(Base):
    __tablename__ = 'orders'
    id = Column(String(255), primary_key=True, index=True)
    contact_number = Column(String(255))
    size_description = Column(String(255))
    status = Column(Integer)
    dropoff_lat = Column(Float)
    dropoff_lng = Column(Float)
    created_at = Column(DateTime)
    last_updated_at = Column(DateTime)
    delivery_center_id = Column(String(255), ForeignKey('delivery_centers.id'))
    delivery_center = relationship("DeliveryCenterTable", back_populates="orders")
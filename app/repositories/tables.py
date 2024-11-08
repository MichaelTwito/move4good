from api.input_objects_schemas import StatusEnum
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Enum, Integer, String, ForeignKey, Float

Base = declarative_base()

class UsersTable(Base):
    __tablename__ = 'users'
    id = Column(String(255), primary_key=True , index=True)
    username = Column(String(255), index=True, unique=True)
    password = Column(String(255))
    role = Column(String(255))
    delivery_centers = relationship('DeliveryCentersTable', back_populates='user')

class DeliveryCentersTable(Base):
    __tablename__ = 'delivery_centers'
    id = Column(String(255), primary_key=True, index=True, default=0)
    name = Column(String(255))
    address = Column(String(255), unique=True)
    lng = Column(Float)
    lat = Column(Float)
    orders = relationship('OrdersTable', back_populates='delivery_center')
    user_id = Column(String(255), ForeignKey('users.id'))
    user = relationship('UsersTable', back_populates='delivery_centers', uselist=False)

class OrdersTable(Base):
    __tablename__ = 'orders'
    id = Column(String(255), primary_key=True, index=True)
    contact_number = Column(String(255))
    size_description = Column(String(255))
    description = Column(String(255))
    dropoff_address = Column(String(255))
    status = Column(Enum(StatusEnum), default=StatusEnum.OPENED)
    dropoff_lat = Column(Float)
    dropoff_lng = Column(Float)
    created_at = Column(Integer)
    last_updated_at = Column(Integer)
    delivery_center_id = Column(String(255), ForeignKey('delivery_centers.id'))
    delivery_center = relationship("DeliveryCentersTable", back_populates="orders")
from sqlalchemy import Column, Integer, String, Float
from .database import Base


class Address(Base):
    
    __tablename__ = 'address'
    
    id = Column(Integer, primary_key = True, index = True)
    address_line_one = Column(String)
    address_line_two = Column(String)
    address_line_three = Column(String)
    city_name = Column(String)
    state_name = Column(String)
    pin_code = Column(String)
    land_mark = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

#  数据库内部书写
from sqlalchemy import Column , Integer , String , Float , DateTime , ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True , index=True)
    # nullable=False 表示该字段不能为空
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    boards = relationship('Board', backref='user', lazy='dynamic')

class Board(Base):
    __tablename__ = 'board'

    id = Column(Integer , primary_key=True, index=True)
    title = Column(String(100) , nullable=False)
    user_id = Column(Integer , ForeignKey('user.id'), nullable=False)

    lists = relationship('List' , backref='board' , lazy='dynamic' , cascade="all, delete-orphan" , order_by="List.order")

class List(Base):
    __tablename__ = 'list'

    id = Column(Integer , primary_key=True, index=True)
    title = Column(String(100) , nullable=False)
    order = Column(Integer , nullable=False)
    board_id = Column(Integer , ForeignKey('board.id'), nullable=False)

    cards = relationship('Card' , backref='list' , lazy='dynamic' , cascade="all, delete-orphan" , order_by="Card.order")

class Card(Base):
    __tablename__ = 'card'

    id = Column(Integer , primary_key=True, index=True)
    content = Column(String(255) , nullable=False)
    order = Column(Integer , nullable=False)
    list_id = Column(Integer ,  ForeignKey('list.id') , nullable=False)

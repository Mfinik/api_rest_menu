# Module containing SQLAlchemy models for the application.


from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


# SQLAlchemy model for submenus.
class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, index=True)
    menu_id = Column(
        Integer, ForeignKey("menus.id", ondelete="CASCADE"), nullable=False
    )
    description = Column(String, nullable=False)

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship(
        "Dish", back_populates="submenu", cascade="all, delete-orphan"
    )


# SQLAlchemy model for menus.
class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)

    submenus = relationship(
        "Submenu", back_populates="menu", cascade="all, delete-orphan"
    )


# SQLAlchemy model for dishes.
class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True, nullable=False)
    price = Column(Float, index=True)
    submenu_id = Column(Integer, ForeignKey("submenus.id", ondelete="CASCADE"))

    submenu = relationship("Submenu", back_populates="dishes")

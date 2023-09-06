# Module containing Pydantic schemas for menu-related data.


from typing import List, Optional, Tuple

from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.models import Dish as DBDish
from app.models import Menu as DBMenu
from app.models import Submenu as DBSubmenu


# Calculate submenus_count and dishes_count
def calculate_counts(db: Session, menu_id: int) -> Tuple[int, int]:
    submenus_count = db.scalar(
        select(func.count(DBSubmenu.id)).where(DBSubmenu.menu_id == menu_id)
    )

    dishes_count = db.scalar(
        select(func.count(DBDish.id))
        .join(DBSubmenu)
        .where(DBSubmenu.menu_id == menu_id)
    )

    return submenus_count, dishes_count


# Get items from db
def get_item_from_db(db: Session, model, **kwargs):
    try:
        stmt = select(model).filter_by(**kwargs)
        result = db.execute(stmt)
        item = result.scalars().first()

        return item

    except NoResultFound:
        return None


# Get menu by id from db
def get_menu_from_db(db: Session, menu_id: int):
    return get_item_from_db(db, DBMenu, id=menu_id)


# Get submenu by id from db
def get_submenu_from_db(db: Session, menu_id: int, submenu_id: int):
    return get_item_from_db(db, DBSubmenu, menu_id=menu_id, id=submenu_id)


# Get dish by id from db
def get_dish_from_db(db: Session, dish_id: int, submenu_id: int):
    return get_item_from_db(db, DBDish, id=dish_id, submenu_id=submenu_id)


# Класс Pydantic для Блюда (используется для входных данных при создании)
class DishCreate(BaseModel):
    title: str
    description: str
    price: float


# Класс Pydantic для Блюда (используется для вывода данных)
class DishBase(BaseModel):
    id: str
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True


# Класс Pydantic для Подменю (используется для входных данных при создании)
class SubMenuCreate(BaseModel):
    title: str
    description: str


# Класс Pydantic для Подменю (используется для вывода данных)
class SubMenuBase(BaseModel):
    id: str
    title: str
    description: str
    dishes_count: int
    dishes: List[DishBase] = []


# Класс Pydantic для Меню (используется для входных данных при создании)
class MenuCreate(BaseModel):
    title: str
    description: str
    submenus: Optional[List[SubMenuCreate]] = None

    class Config:
        orm_mode = True


# Класс Pydantic для Меню (используется для вывода данных)
class MenuBase(BaseModel):
    id: str
    title: str
    description: str
    submenus: Optional[List[SubMenuBase]] = None

    class Config:
        orm_mode = True


# Ответы от сервера (Response модели)
class DishResponse(BaseModel):
    id: str
    title: str
    description: str
    price: str
    dishes_count: int  # Add the dishes_count field


class SubMenuResponse(BaseModel):
    id: str
    title: str
    description: str
    dishes_count: int = 0


class MenuResponse(BaseModel):
    id: str
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0

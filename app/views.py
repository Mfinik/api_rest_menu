# Module containing view functions for menu-related operations.


from typing import List

from fastapi import HTTPException
from sqlalchemy import delete, func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import schemas
from app.models import Dish as DBDish
from app.models import Menu as DBMenu
from app.models import Submenu as DBSubmenu


# Create new menu
def post_create_menu(db: Session,
                     menu: schemas.MenuCreate) -> schemas.MenuResponse:
    db_menu = DBMenu(title=menu.title, description=menu.description)
    db.add(db_menu)
    try:
        db.commit()
        db.refresh(db_menu)

        submenus_count, dishes_count = schemas.calculate_counts(db, db_menu.id)

        return schemas.MenuResponse(
            id=str(db_menu.id),
            title=db_menu.title,
            description=db_menu.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count,
        )
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Menu with this title already exists"
        ) from exc


# Get menu list with submenus count and dishes count for each
def get_menus_with_counts(
    db: Session, skip: int = 0, limit: int = 10
) -> List[schemas.MenuResponse]:
    stmt_menus = select(DBMenu).offset(skip).limit(limit)
    result_menus = db.execute(stmt_menus)
    db_menus = result_menus.scalars().all()

    # Calculate submenus_count and dishes_count for each menu
    menu_responses = []
    for menu in db_menus:
        submenus_count, dishes_count = schemas.calculate_counts(db, menu.id)

        menu_response = schemas.MenuResponse(
            id=str(menu.id),
            title=menu.title,
            description=menu.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count,
        )
        menu_responses.append(menu_response)

    return menu_responses


# Get menu by id
def get_menu_by_id(db: Session, menu_id: int) -> schemas.MenuResponse:
    db_menu = schemas.get_menu_from_db(db, menu_id)

    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    # Calculate submenus_count and dishes_count
    submenus_count, dishes_count = schemas.calculate_counts(db, db_menu.id)

    return schemas.MenuResponse(
        id=str(db_menu.id),
        title=db_menu.title,
        description=db_menu.description,
        submenus_count=submenus_count,
        dishes_count=dishes_count,
    )


# Update_menu
def update_menu_by_id(
    db: Session, menu_id: int, menu: schemas.MenuCreate
) -> schemas.MenuResponse:
    db_menu = schemas.get_menu_from_db(db, menu_id)

    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    db_menu.title = menu.title
    db_menu.description = menu.description

    try:
        db.commit()
        db.refresh(db_menu)

        return schemas.MenuResponse(
            id=str(db_menu.id), title=db_menu.title,
            description=db_menu.description)

    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Menu with this title already exists"
        ) from exc


# Delete menu
def delete_menu_by_id(db: Session, menu_id: int) -> schemas.MenuResponse:
    # Check if the menu exists before deleting
    deleted_menu = schemas.get_menu_from_db(db, menu_id)
    if not deleted_menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    # Update all submenus related to the menu being deleted
    # and set their menu_id to None
    stmt_update_submenus = (
        update(DBSubmenu).where(
            DBSubmenu.menu_id == menu_id).values(menu_id=None)
    )
    db.execute(stmt_update_submenus)

    # Delete the menu
    stmt_delete_menu = delete(DBMenu).where(DBMenu.id == menu_id)
    db.execute(stmt_delete_menu)

    # Commit the transaction to apply the changes
    db.commit()

    return {"status": True, "message": "The menu has been deleted"}


def post_create_submenu(
    db: Session, menu_id: int, submenu: schemas.SubMenuCreate
) -> schemas.SubMenuResponse:
    db_submenu = DBSubmenu(
        title=submenu.title, description=submenu.description, menu_id=menu_id
    )
    db.add(db_submenu)

    try:
        db.commit()
        db.refresh(db_submenu)

        dishes_count = db.scalar(
            select(func.count(DBDish.id))
            .join(DBSubmenu)
            .where(DBSubmenu.menu_id == db_submenu.menu_id)
        )

        return schemas.SubMenuResponse(
            id=str(db_submenu.id),
            title=db_submenu.title,
            description=db_submenu.description,
            dishes_count=dishes_count,
        )
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Subenu with this title already exists"
        ) from exc


# Get submenu list with dishes count for each
def get_submenus_with_counts(
    db: Session, menu_id: int, skip: int = 0, limit: int = 10
) -> schemas.SubMenuResponse:
    stmt = (
        select(DBSubmenu).filter(
            DBSubmenu.menu_id == menu_id).offset(skip).limit(limit)
    )
    result = db.execute(stmt)
    submenus = result.scalars().all()

    submenu_responses = []
    for submenu in submenus:
        dishes_count = db.scalar(
            select(func.count(DBDish.id))
            .join(DBSubmenu)
            .where(DBSubmenu.menu_id == submenu.menu_id)
        )

        submenu_response = schemas.SubMenuResponse(
            id=str(submenu.id),
            title=submenu.title,
            description=submenu.description,
            dishes_count=dishes_count,
        )
        submenu_responses.append(submenu_response)

    return submenu_responses


# Get submenu by id
def get_submenu_by_id(
    db: Session, menu_id: int, submenu_id: int
) -> schemas.SubMenuResponse:
    db_submenu = schemas.get_submenu_from_db(db, menu_id, submenu_id)

    if not db_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    # Получаем количество блюд для данного подменю
    dishes_count = db.scalar(
        select(func.count(DBDish.id)).join(
            DBSubmenu).where(DBSubmenu.id == submenu_id)
    )

    return schemas.SubMenuResponse(
        id=str(db_submenu.id),
        title=db_submenu.title,
        description=db_submenu.description,
        dishes_count=dishes_count,
    )


# Update submenu by id
def update_submenu_by_id(
    db: Session, menu_id: int, submenu_id: int, submenu: schemas.SubMenuCreate
) -> schemas.SubMenuResponse:
    db_submenu = schemas.get_submenu_from_db(db, menu_id, submenu_id)
    if not db_submenu:
        raise HTTPException(status_code=404, detail="Submenu not found")

    db_submenu.title = submenu.title
    db_submenu.description = submenu.description

    try:
        db.commit()
        db.refresh(db_submenu)
        return schemas.SubMenuResponse(
            id=str(db_submenu.id),
            title=db_submenu.title,
            description=db_submenu.description,
            dishes_count=0,
        )
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Subenu with this title already exists"
        ) from exc


# Delete submenu
def delete_submenu_by_id(
    db: Session, menu_id: int, submenu_id: int
) -> schemas.SubMenuResponse:
    # Check if the menu exists before deleting
    deleted_submenu = schemas.get_submenu_from_db(db, menu_id, submenu_id)
    if not deleted_submenu:
        raise HTTPException(status_code=404, detail="Submenu not found")

    # Update all rows in the "dishes" table related to the deleted submenu
    stmt_update = (
        update(DBDish)
        .where(DBDish.submenu_id == submenu_id)
        .values(submenu_id=None)
        .where(DBDish.submenu_id == submenu_id)
    )

    db.execute(stmt_update)

    # Delete submenu
    stmt_delete = delete(DBSubmenu).where(
        DBSubmenu.menu_id == menu_id, DBSubmenu.id == submenu_id
    )

    db.execute(stmt_delete)

    # Commit the transaction to apply the changes
    db.commit()

    return {"status": True, "message": "The submenu has been deleted"}


# Create dish
def create_dish(
    db: Session, submenu_id: int, dish: schemas.DishCreate
) -> schemas.DishResponse:
    db_dish = DBDish(
        title=dish.title,
        price=dish.price,
        submenu_id=submenu_id,
        description=dish.description,
    )
    db.add(db_dish)

    try:
        db.commit()
        db.refresh(db_dish)

        return schemas.DishResponse(
            id=str(db_dish.id),
            title=db_dish.title,
            description=db_dish.description,
            price=str(db_dish.price),
            dishes_count=0,
        )
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Dish with this title already exists"
        ) from exc


# Get dishes list
def get_dishes_with_counts(
    db: Session, submenu_id: int, skip: int = 0, limit: int = 10
) -> schemas.DishResponse:
    stmt = (
        select(DBDish).filter(
            DBDish.submenu_id == submenu_id).offset(skip).limit(limit)
    )
    result = db.execute(stmt)
    dishes = result.scalars().all()

    if not dishes:
        return []

    stmt = select(func.count()).where(DBDish.submenu_id == submenu_id)
    result = db.execute(stmt)
    dish_count = result.scalar() or 0

    return [
        schemas.DishResponse(
            id=str(dish.id),
            title=dish.title,
            description=dish.description,
            price=str(dish.price),
            dishes_count=dish_count,
        )
        for dish in dishes
    ]


# Get dish by id
def get_dish_by_id(db: Session, dish_id: int,
                   submenu_id) -> schemas.DishResponse:
    db_dish = schemas.get_dish_from_db(db, dish_id, submenu_id)

    if not db_dish:
        raise HTTPException(status_code=404, detail="dish not found")

    return schemas.DishResponse(
        id=str(db_dish.id),
        title=db_dish.title,
        description=db_dish.description or "",
        price=str(db_dish.price),
        dishes_count=0,
    )


# Update dish
def update_dish_by_id(
    db: Session, dish_id: int, submenu_id: int, dish: schemas.DishCreate
) -> schemas.DishResponse:
    db_dish = schemas.get_dish_from_db(db, dish_id, submenu_id)

    if not db_dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    db_dish.title = dish.title
    db_dish.description = dish.description
    db_dish.price = dish.price

    try:
        db.commit()
        db.refresh(db_dish)
        return schemas.DishResponse(
            id=str(db_dish.id),
            title=db_dish.title,
            description=db_dish.description,
            price=str(db_dish.price),
            dishes_count=0,
        )
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Dish with this title already exists"
        ) from exc


# Delete dish
def delete_dish_by_id(
    db: Session, dish_id: int, submenu_id: int
) -> schemas.DishResponse:
    stmt = (
        delete(DBDish)
        .where(DBDish.id == dish_id, DBDish.submenu_id == submenu_id)
        .returning(DBDish)
    )

    result = db.execute(stmt)
    deleted_dish = result.scalars()
    if not deleted_dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    db.commit()
    return {"status": True, "message": "The dish has been deleted"}

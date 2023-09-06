# Module containing FastAPI routers for menu-related endpoints.


from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import schemas, views
from app.database import get_db

router = APIRouter()


# Create new menu
@router.post("/api/v1/menus/", response_model=schemas.MenuResponse, status_code=201)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    return views.post_create_menu(db, menu)


# Get menus list with counts
@router.get("/api/v1/menus/", response_model=List[schemas.MenuResponse])
def read_menus(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return views.get_menus_with_counts(db, skip, limit)


# Get menu by id
@router.get("/api/v1/menus/{menu_id}", response_model=schemas.MenuResponse)
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    return views.get_menu_by_id(db, menu_id)


# Update menu
@router.patch("/api/v1/menus/{menu_id}", response_model=schemas.MenuResponse)
def update_menu(menu_id: int, menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    return views.update_menu_by_id(db, menu_id, menu)


# Delete menu
@router.delete("/api/v1/menus/{menu_id}", status_code=status.HTTP_200_OK)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    return views.delete_menu_by_id(db, menu_id)


# Create new submenu
@router.post(
    "/api/v1/menus/{menu_id}/submenus/",
    response_model=schemas.SubMenuResponse,
    status_code=201,
)
def create_submenu(
    menu_id: int, submenu: schemas.SubMenuCreate, db: Session = Depends(get_db)
):
    return views.post_create_submenu(db, menu_id, submenu)


# Get submenus list with counts
@router.get(
    "/api/v1/menus/{menu_id}/submenus/", response_model=List[schemas.SubMenuResponse]
)
def read_submenus(
    menu_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return views.get_submenus_with_counts(db, menu_id, skip, limit)


# Get submenu by id
@router.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.SubMenuResponse,
)
def read_submenu_by_id(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    return views.get_submenu_by_id(db, menu_id, submenu_id)


# Update submenu
@router.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.SubMenuResponse,
)
def update_submenu(
    menu_id: int,
    submenu_id: int,
    submenu: schemas.SubMenuCreate,
    db: Session = Depends(get_db),
):
    return views.update_submenu_by_id(db, menu_id, submenu_id, submenu)


# Delete submenu
@router.delete(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}", status_code=status.HTTP_200_OK
)
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    return views.delete_submenu_by_id(db, menu_id, submenu_id)


# Create new dish
@router.post(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/",
    response_model=schemas.DishResponse,
    status_code=201,
)
def create_dish(
    submenu_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)
):
    return views.create_dish(db, submenu_id, dish)


# Get dishes list
@router.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/",
    response_model=List[schemas.DishResponse],
)
def read_dishes(
    submenu_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return views.get_dishes_with_counts(db, submenu_id, skip, limit)


# Get dish by id
@router.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.DishResponse,
)
def read_dish(dish_id: int, submenu_id: int, db: Session = Depends(get_db)):
    return views.get_dish_by_id(
        db,
        dish_id,
        submenu_id,
    )


# Update dish
@router.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.DishResponse,
)
def update_dish(
    dish_id: int,
    submenu_id: int,
    dish: schemas.DishCreate,
    db: Session = Depends(get_db),
):
    return views.update_dish_by_id(db, dish_id, submenu_id, dish)


# Delete dish
@router.delete(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    status_code=status.HTTP_200_OK,
)
def delete_dish(dish_id: int, submenu_id: int, db: Session = Depends(get_db)):
    return views.delete_dish_by_id(db, dish_id, submenu_id)

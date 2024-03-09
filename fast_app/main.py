"""
Main module to fast_app application
"""

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from fast_app.db.item import DBItem
from fast_app.models.item import Item, ItemCreate, ItemUpdate
from fast_app.utils import helper

DATABASE_URL = "sqlite:///dev.db"
engine = helper.get_engine(DATABASE_URL)
SessionLocal = helper.make_session(engine)
app = FastAPI()


def get_db():
    """
    Generator to yield database session
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


@app.get("/")
def home():
    """
    Appplication's root
    """
    return "application working"


@app.post("/items")
def create_item(item: ItemCreate, db: Session = Depends(get_db)) -> Item:
    """
    Creates an item
    """
    db_item = DBItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return Item(**db_item.__dict__)


@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    """
    Reads an item
    """
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return Item(**db_item.__dict__)


@app.put("/items/{item_id}")
def update_item(
    item_id: int, item: ItemUpdate, db: Session = Depends(get_db)
) -> Item:  # noqa: E501
    """
    Updates an item
    """
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return Item(**db_item.__dict__)


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    """
    Deletes an item
    """
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return Item(**db_item.__dict__)

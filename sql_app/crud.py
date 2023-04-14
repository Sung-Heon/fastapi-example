from sqlalchemy.orm import Session
from .database import engine
from . import models, schemas
from sqlalchemy import text

def get_user_sql(db: Session, user_id: int):
    sql_user = text(f"""SELECT * FROM users WHERE users.id={user_id}""")
    sql_item = text(f"""SELECT * FROM items WHERE items.owner_id={user_id}""")

    with engine.connect() as con:
        user = con.execute(sql_user)
        item = con.execute(sql_item)
    user_dict = dict(user.mappings().all()[0])
    item_dict = item.mappings().all()
    user_dict["items"] = item_dict
    return user_dict


def get_user_by_email_sql(db: Session, email: str):
    sql_user = text(f"""SELECT * FROM users WHERE users.email='{email}' """)
    with engine.connect() as con:
        user = con.execute(sql_user)
    return dict(user.all())


def get_users_sql(db: Session, skip: int = 0, limit: int = 100):
    sql_user = text(f"""SELECT * FROM users LIMIT {limit} OFFSET {skip}""")
    with engine.connect() as con:
        user = con.execute(sql_user)
    return user.mappings().all()


def create_user_sql(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    sql = text(f"""INSERT INTO users (email, hashed_password, is_active) VALUES ('{user.email}', '{fake_hashed_password}', TRUE)""")
    with engine.connect() as con:
        with con.begin():
            con.execute(sql)
    return get_users_sql(None)[-1]


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)sql = text("UPDATE users SET email = :new_email, hashed_password = :new_hashed_password WHERE id = :user_id")

#     return db_item


def delete_user_item_sql(db: Session, item_id: int):
    sql = text(f"""DELETE FROM items WHERE items.id = {item_id}""")
    with engine.connect() as con:
        with con.begin():
            con.execute(sql)
    return "204"

def update_item_sql(db: Session, item_id: int, item: schemas.ItemUpdate):
    sql = text(f"""UPDATE items SET title='{item.title}', description='{item.description}' WHERE id = {item_id}""")    
    with engine.connect() as con:
        with con.begin():
            con.execute(sql)
    sql_item = text(f"""SELECT * FROM items WHERE id = {item_id}""")
    with engine.connect() as con:
        db_item = con.execute(sql_item)
    return dict(db_item.mappings().all()[0])

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_user_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    db.delete(db_item)
    db.commit()
    return db_item

def update_item(db: Session, item_id: int, item: schemas.ItemUpdate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    item_data = item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    db.add(db_item)
    db.commit()
    return db_item
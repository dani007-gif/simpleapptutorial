from fastapi import FastAPI, Depends
from models import Item, Base, User
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "mysql+mysqlconnector://root:Daniel%408606@localhost:3306/fastapi_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(first_name: str, last_name: str, City:str, db: Session = Depends(get_db)):
    new_user = User(first_name=first_name, last_name=last_name, City=City)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created", "user": new_user}

@app.post("/items/")
def create_item(item: Item):
    return {"name": item.name, "price": item.price }

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI54321!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/products/{product_id}")
def read_product(product_id: int, q: str = None):
    return {"product_id": product_id, "q": q}
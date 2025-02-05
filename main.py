from fastapi import FastAPI, Depends
from models import Item, User
from sqlalchemy.orm import Session
from database import get_db
from database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

#create a new user
@app.post("/users/")
def create_user(name: str, email: str, password:str, db: Session = Depends(get_db)):
    new_user = User(name=name, email=email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created", "user": new_user}
# get all users
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.post("/items/")
def create_item(item: Item):
    return {"name": item.name, "price": item.price }

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI54321!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


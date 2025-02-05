from fastapi import FastAPI, Depends, Request, Form
from models import Item, User
from sqlalchemy.orm import Session
from database import get_db
from database import engine, Base
from fastapi.responses import JSONResponse, RedirectResponse
from passlib.context import CryptContext
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def serve_login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


#register a new user
@app.post("/register/")
def register_user(name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    hashed_password = get_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered ", "user": new_user}

#Handling Login
@app.post("/login/")
def login_user(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not verify_password(password, user.password):
        return JSONResponse(status_code=401, content={"error": "Invalid credentials"})

    return RedirectResponse(url="/Login.html", status_code=302)


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


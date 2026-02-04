from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import secrets
import models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.post(
    "/users/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):

    role = db.query(models.Role).filter(models.Role.id == user.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    final_password = user.password or secrets.token_urlsafe(8)

    db_user = models.User(
        name=user.name, email=user.email, password=final_password, role_id=user.role_id
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/roles/{role_id}", response_model=schemas.RoleResponse)
def get_role(role_id: int, db: Session = Depends(database.get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@app.get("/users/{user_id}/role", response_model=schemas.RoleResponse)
def get_user_role(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.role

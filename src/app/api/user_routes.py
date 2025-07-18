from fastapi import APIRouter, Depends, HTTPException
from ..db.database import get_session
from ..models.user import Users
from ..utils.auth import hash_pass

user_router = APIRouter()


@user_router.post("/users/",response_model=Users)
def create_user(user : Users, session = Depends(get_session)):
    user.hashed_password = hash_pass(user.hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@user_router.get("/users/{user_id}",response_model=Users)
def read_user(user_id : int , session = Depends(get_session)):
    user_curr = session.get(Users,user_id)
    if not user_curr:
        raise HTTPException(status_code=404, detail="User not found")
    return user_curr
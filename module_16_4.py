from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from typing import Annotated
from pydantic import BaseModel
from typing import List

app = FastAPI()
# uvicorn module_16_4:app --reload


users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int = None


@app.get('/users')
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def post_user(user: User, username: str, age: int) -> User:
    len_users = len(users)
    if len_users == 0:
        user.id = 1
    else:
        user.id = users[len_users - 1].id + 1
    user.username = username
    user.age = age
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int, user: str = Body()):
    edit = user
    for new_user in users:
        if new_user.id == user_id:
            new_user.username = username
            new_user.age = age
            return new_user
    if edit:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delite_user(user_id: int) -> str:
    try:
        users.pop(user_id)
        return f'user {user_id}'

    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')

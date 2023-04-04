from fastapi import APIRouter, status, HTTPException
from db.models.user_model import User
from db.client_db import db_client
from db.schemas.user_schema import user_schema, users_schema
from bson import ObjectId

# Algoritmo de encrytacion

router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Page not found"}})


def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "User not found."}


@router.get("/", response_model=list[User], status_code=status.HTTP_200_OK)
async def users():
    return users_schema(db_client.users.find())


@router.get("/{id}")  # Path
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):

    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')

    # transformar nuestro usuario que recibe el method post en diccionario.
    user_dict = dict(user)
    # se elimina el campo id.
    del user_dict["id"]
    # se agrega el usuario a la base de datos haciendo la operacion para que el mismo mongo nos autogestione un ID unico.
    id = db_client.users.insert_one(user_dict).inserted_id
    # Se crea una instancia utilizando un Schema de tipo Dict. Solicitando los datos en una query por id (el campo id en mongo se solicita con barra baja _id)
    new_user = user_schema(db_client.users.find_one({"_id": id}))
    
    return User(**new_user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        return {"error": "User not delete."}
    



@router.put("/", response_model=User, status_code=status.HTTP_200_OK)
async def user(user: User):
    
    user_dict = dict(user)
    del user_dict["id"]

    try:
        found = db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "User has not beed updated"}
    
    return search_user("_id", ObjectId(user.id))


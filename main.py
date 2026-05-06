from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse, Response
from http.client import HTTPException, HTTPResponse
from typing import List, Optional
from fastapi_pagination import add_pagination, Page
from schemas.schema import UserDataSchema, MeteringDeviceSchema
from dbapi.deps import get_async_session, Base, engine
from models.model import UserDataModel, MeteringDeviceModel, SensorDeviceModel, MeterTypeStatus, SensorTypeStatus
from dbapi.crud import get_user_data, get_metering_all
from sqlalchemy.ext.asyncio import AsyncSession
from pwdlib import PasswordHash
from sqlalchemy import update, select, delete, insert
import dotenv
from dotenv import dotenv_values
from fastapi_pagination import pagination_ctx


env_conf = dotenv_values(".env_config")



# Password hasher machine
password_hasher = PasswordHash.recommended()

# Метаданные приложения
description = 'Backend app'
title = "RestAPI приложение - Metering Station App"

app = FastAPI(title=title, description=description)



# OK !
@app.get("/index",name="Index Handler", tags=["Test Index"])
async def index_route():
    return {"Response": "Hello there!"}



# OK !
@app.post("/login-user",name="Login User",tags=["User Data handlers"],status_code=status.HTTP_202_ACCEPTED)  #pagination_ctx(Page[UserDataSchema]))])
async def login_user_route(login: str, password: str, session: AsyncSession = Depends(get_async_session)):
    """Login User Router: returns 202_accepted http response,\n
       also returns json object with user data. \n
    Args:\n
        login (str): form value \n
        password (str): form velue \n
        session (AsyncSession, optional): _description_. Defaults to Depends(get_async_session).\n

    Returns:\n
        _type_: HTTP_202\n
    """
    actual_user = await get_user_data(session=session,login=login)
    if password_hasher.verify(password, actual_user.password):
        return actual_user
    

# OK !
@app.put("/update-user",name="Update User", status_code=status.HTTP_201_CREATED ,tags=["User Data handlers"])
async def update_user_route(new_user: UserDataSchema, session: AsyncSession = Depends(get_async_session)):
    """Update user data router:\n
    Args:\n
        new_user (UserDataSchema): _description_\n
        session (AsyncSession, optional): _description_. Defaults to Depends(get_async_session).\n
    Returns:\n
        _type_: HTTP_201_CREATED\n
    """
    stmt = update(UserDataModel).where(UserDataModel.id == new_user.id).values(**new_user.model_dump())
    async with session as db:
        await db.execute(stmt)
        await db.commit()
    return new_user  


# OK !
@app.post("/meter-add",name="Metering add", status_code=status.HTTP_201_CREATED ,tags=["Meters & Sensors handlers"])
async def meter_add_route(metering_device: MeteringDeviceSchema, session: AsyncSession = Depends(get_async_session)):
    """Metering device adding router:\n
    Args:\n
        metering_device (MeteringDeviceSchema): _description_\n
        session (AsyncSession, optional): _description_. Defaults to Depends(get_async_session).\n
    Returns:\n
        _type_: HTTP_201_CREATED\n
    """
    async with session as db:
        new_device = MeteringDeviceModel(**metering_device.model_dump())
        db.add(new_device)
        await db.commit()
        await db.refresh(new_device)
        return new_device


# Получить все счетчики - значение items
@app.get("/meters-list",name="Meters List", 
         status_code=status.HTTP_200_OK, 
         tags=["Meters & Sensors handlers"],
         response_model=List[MeteringDeviceSchema]) 

async def meters_list_route(session: AsyncSession = Depends(get_async_session)):
    """ Get all metering devices list:\n
    Args:\n
        session (AsyncSession, optional): _description_. Defaults to Depends(get_async_session).\n
    Returns:\n
        _type_: List[MeterinDeviceSchema]\n
    """
    result_list = await get_metering_all(session=session)
    return result_list


# OK !
@app.put("/update-meter",name="Update Meter", status_code=status.HTTP_202_ACCEPTED ,tags=["Meters & Sensors handlers"])
async def meter_update_route(updated_item: MeteringDeviceSchema, session: AsyncSession = Depends(get_async_session)):
    """
    Update metering device:\n
    Args:\n
        updated_item: MeteringDeviceSchema json object\n
        session (AsyncSession, optional): _description_. Defaults to Depends(get_async_session).\n
        ---////---\n
        cold_water = "холодная вода" \n
        hot_water = "горячая вода" \n
        electricity = "электричество" \n
        heat_metering = "тепловая энергия" \n
    Returns:\n
        _type_: List[MeterinDeviceSchema] \n
    """
    #updated_item.
    async with session as db:
        stmt = update(MeteringDeviceModel).where(MeteringDeviceModel.id == updated_item.id).values(**updated_item.model_dump())
        await db.execute(stmt)
        await db.commit()
    return updated_item




@app.delete("/delete-meter/{deleted_item_id}",name="Delete Meter", status_code=status.HTTP_202_ACCEPTED ,tags=["Meters & Sensors handlers"])
async def meter_delete_route(deleted_item_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Delete metering device:\n
    Args:\n
        deleted_item_id: int\n
        session (AsyncSession, optional): _description_. Defaults to Depends(get_async_session).\n
    Returns:\n
        _type_: HTTP_200_OK \n
    """
    async with session as db:
        deleted_item = await db.get(MeteringDeviceModel, deleted_item_id)
        if deleted_item is not None:
            await db.delete(deleted_item)
            await db.commit()
            return deleted_item
        else:
            return {"details":"No item found"}






@app.on_event("startup")
async def startup():
    """On Starup Method to create all tables in DB"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        hashed_string = password_hasher.hash(env_conf["DEFAULT_PASSWORD"])
        stmt = insert(UserDataModel).values(login=env_conf['DEFAULT_LOGIN'], password=hashed_string)
        await conn.execute(statement=stmt)

    







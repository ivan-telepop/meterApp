from sqlalchemy.future import select
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from models.model import UserDataModel, MeteringDeviceModel, SensorDeviceModel
from schemas.schema import UserDataSchema, MeteringDeviceSchema, SensorDeviceSchema
from typing import List, Optional



# Получение юзера
async def get_user_data(session: AsyncSession, login: Optional[str] = None):
    """Асинхронная функция для получения user data \n
     параметры извлечения:
     loin: str \n
     password: str \n
     """
    async with session as db:
        stmt = select(UserDataModel).where((UserDataModel.login == login))
        res = await db.execute(stmt)
        retr_user = res.scalars().first()
        return retr_user

# Создание юзера
async def create_user_data(
        session: AsyncSession, 
        login: Optional[str] = None, 
        password: Optional[str] = None,
        address: Optional[str] = None, 
        token: Optional[str] = None,
        ):
    """Асинхронная функция для create user data \n
     параметры:
     loin: str \n
     password: str \n
     """
    new_user_data = UserDataModel(login,password,address,token)
    async with session as db:
        db.add(new_user_data)
        await db.commit()
    return new_user_data


# СЧЕТЧИКИ 

#  Получение одного девайса по типу и имени
async def get_metering_device(session: AsyncSession, name: Optional[str] = None, type: Optional[str] = None):
    """Асинхронная функция для получения metering device по типу и имени. \n
     параметры извлечения:
     name: str \n
     type: str \n
     """
    async with session as db:
        stmt = select(MeteringDeviceModel).where((MeteringDeviceModel.name == name) | (MeteringDeviceModel.type == type))
        res = await db.execute(stmt)
        device = res.scalars().first()
        return device



async def get_metering_all(session: AsyncSession) -> List[MeteringDeviceSchema]:
    """Metering Devices get all"""
    stmt = select(MeteringDeviceModel)
    async with session as db:
        result = await db.execute(stmt)
        return result.scalars().all()

    
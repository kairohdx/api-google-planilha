
from typing import Any

from fastapi import HTTPException
from app.data.data import DbData
from app.models.user import UserBase, UserLogin, UserPost


class DataUser(DbData):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.collection.create_index("email", unique=True)

    async def getBySearch(self, q:str = "", page:int = 0, limit:int = 10) -> list[UserBase]:
        users = await self.collection.find(filter={"$or":[{"name":q}, {"email":q}]}, skip=page, limit=limit).to_list()

        return [UserBase.parse_obj(u) for u in users]
    
    async def getById(self, id:str) -> UserBase:
        if (user := await self.collection.find_one({"_id":id})) is not None:            
            return UserBase.parse_obj(user)
        
        raise HTTPException(status_code=404, detail=f'Usuario de id "{id}" não encontrado')
    
    async def getByEmail(self, email:str) -> UserLogin:
        if (user := await self.collection.find_one({"email":email})) is not None:
            return UserLogin.parse_obj(user)
        
        raise HTTPException(status_code=404, detail=f'Usuario de E-mail "{email}" não encontrado')
    
    async def insertUser(self, userData:UserPost) -> UserBase:
        if not await self.getByEmail(userData.email):
            if (user := await self.collection.insert_one(userData.dict())):
                return await self.collection.find_one({"_id":user.inserted_id})
        raise HTTPException(status_code=409, detail=f'E-mail "{userData.email}" já cadastrado')

    async def updateUser(self, id:str, userData:UserPost) -> UserBase:
        update_result = await self.collection.update_one({"_id": id}, {"$set": userData})

        if update_result.modified_count:
            if user := (await self.collection.find_one({"_Id":id})) is not None:
                return UserBase.parse_obj(user)
            
        if user := (await self.collection.find_one({"_Id":id})) is not None:
                return UserBase.parse_obj(user)
        
        raise HTTPException(status_code=404, detail=f'Usuario de id "{id}" não encontrado')
    
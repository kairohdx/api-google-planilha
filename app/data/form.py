
from typing import Any

from fastapi import HTTPException

from app.data.data import DbData
from app.models.form import FormComplete, FormLayoutBase

class DataForm(DbData):
    def __init__(self):
        super().__init__(self.__class__.__name__)

    async def getBySearch(self, q:str = "", page:int = 0, limit:int = 10) -> list[FormLayoutBase]:
        forms = await self.collection.find(filter={"$or":[{"name":q}, {"email":q}]}, skip=page, limit=limit).to_list()

        return [FormLayoutBase.parse_obj(u) for u in forms]
    
    async def getById(self, id:str) -> FormComplete:
        if (form := await self.collection.find_one({"_id":id})) is not None:            
            return FormComplete.parse_obj(form)
        
        raise HTTPException(status_code=404, detail=f'Usuario de id "{id}" não encontrado')
    
    async def insertForm(self, formData:FormComplete) -> FormComplete:
        form = await self.collection.insert_one(formData.dict())
        if form:
            return await self.getById(str(form.inserted_id))

    async def updateForm(self, id:str, formData:FormComplete) -> FormComplete:
        update_result = await self.collection.update_one({"_id": id}, {"$set": formData})

        if update_result.modified_count:
            if form := (await self.collection.find_one({"_Id":id})) is not None:
                return FormComplete.parse_obj(form)
            
        if form := (await self.collection.find_one({"_Id":id})) is not None:
                return FormComplete.parse_obj(form)
        
        raise HTTPException(status_code=404, detail=f'Usuario de id "{id}" não encontrado')

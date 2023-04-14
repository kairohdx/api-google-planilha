from fastapi import APIRouter

router = APIRouter(
    prefix="/forms",
    tags=["forms"],
    dependencies=[Depends(get)]
)

@router.get("/" )
async def read_forms():
    return [{"form1":"sucesso"}]

@router.get("/{idform}")
async def read_form(idForm: str):
    return {"_id": idForm}
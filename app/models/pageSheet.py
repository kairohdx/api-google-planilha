
from pydantic import BaseModel


class PageSheet(BaseModel):
    pageName:str = "Nova Pagina"
    firstLine:list[str] = ["Coluna1", "Coluna2"]
    values:list[str] = []

from pydantic import BaseModel


class Option(BaseModel):
    value: str = ''
    text: str = 'option'


class Input(BaseModel):
    name: str = 'inputName'
    placeHolder: str = ''
    id: str = 'inputId'
    type: str = 'text'
    options: list[Option] = []
    label: str = 'inputLabel'
    limit: int | None = None


class FormLayoutBase(BaseModel):
    name: str
    description: str | None = None

class FormComplete(FormLayoutBase):
    inputs: list[Input]

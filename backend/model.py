from typing import TYPE_CHECKING,Optional

if TYPE_CHECKING:
    from sqlmodel import SQLModel, Field

from sqlmodel import SQLModel, Field
# class Todo(SQLModel,table=True):
#     id : Optional[int]     = Field(default=None,primary_key=True)
#     title:str              = Field(max_length= 232 ,nullable=False)
#     description:str | None = None
#     completed:bool         = Field(default=False)

class Book(SQLModel, table= True):
    id:Optional["int"] = Field(primary_key=True,default=None)
    title:str = Field(nullable=False)
    author:str = Field(max_length=52,nullable=False)
    genre:str = Field(nullable=False)
    publication_year:int = Field(nullable=False)
    read_status:bool = Field(nullable=False,default=False)
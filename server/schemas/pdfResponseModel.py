from pydantic import BaseModel
from server.schemas.pdfItemModel import PdfItemModel


class pdfResponseModel(BaseModel):
    PdfList : list[PdfItemModel]
    access_token: str
    token_type: str
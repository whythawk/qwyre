from pydantic import BaseModel, EmailStr


class EmailContent(BaseModel):
    email: EmailStr
    subject: str
    content: str

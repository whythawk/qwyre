from app.schema_types import BaseEnum


class MimeType(BaseEnum):
    EPUB = "application/epub+zip"
    DOC = "application/msword"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

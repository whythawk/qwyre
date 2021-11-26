from app.schema_types import BaseEnum


class WorkStateType(BaseEnum):
    SUBMITTED = ""
    OFFERED = ""
    CONTRACTED = ""
    EDITED = ""
    PUBLISHED = ""
    WITHDRAWN = ""
    REVIEWED = ""
    SUSPENDED = ""

    def describe(self):
        description = {
            "SUBMITTED": "Uploaded work for submission.",
            "OFFERED": "Offered work for editing.",
            "CONTRACTED": "Agreed a monetisation proportional income share with collaborators.",
            "EDITED": "Editing and work EPUB complete.",
            "PUBLISHED": "Work published and available.",
            "WITHDRAWN": "Work has been withdrawn pending review.",
            "REVIEWED": "Review has been completed.",
            "SUSPENDED": "Work has been permanently withdrawn.",
        }
        return description[self.value]

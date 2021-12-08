from app.schema_types import BaseEnum


class WorkStateType(BaseEnum):
    SUBMITTED = "submitted"
    UPDATED = "updated"
    OFFERED = "offered"
    CONTRACTED = "contracted"
    DEPARTED = "departed"
    EDITED = "edited"
    PRICED = "priced"
    PUBLISHED = "published"
    PENDING = "pending"
    WITHDRAWN = "withdrawn"
    REVIEWED = "reviewed"
    SUSPENDED = "suspended"

    def describe(self):
        description = {
            "SUBMITTED": "Uploaded work for submission.",
            "UPDATED": "Updated by one of the collaborators.",
            "OFFERED": "Offered work for editing.",
            "CONTRACTED": "Agreed a monetisation proportional income share with collaborators.",
            "DEPARTED": "A party to the contract departed.",
            "EDITED": "Editing and work EPUB complete.",
            "PRICED": "Pricing for work EPUB agreed and complete.",
            "PUBLISHED": "Work published and available.",
            "PENDING": "Changes need to be approved by relevant collaborators.",
            "WITHDRAWN": "Work has been withdrawn pending review.",
            "REVIEWED": "Review has been completed.",
            "SUSPENDED": "Work has been permanently withdrawn.",
        }
        return description[self.value]

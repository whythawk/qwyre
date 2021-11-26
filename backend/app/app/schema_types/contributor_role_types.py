from app.schema_types import BaseEnum


class ContributorRoleType(BaseEnum):
    """
    List of terms for the contributor roles.
    """

    AUTHOR = "author"
    ARTIST = "artist"
    CURATOR = "curator"
    EDITOR = "editor"
    TRANSLATOR = "translator"
    MODERATOR = "moderator"

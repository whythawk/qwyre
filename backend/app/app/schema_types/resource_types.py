from enum import auto

from app.schema_types import BaseEnum


class ResourceType(BaseEnum):
    TEAM = auto()
    PROJECT = auto()
    COLLECTION = auto()
    DATASET = auto()
    DATA = auto()
    SCHEMA = auto()
    METHOD = auto()

    def describe(self):
        description = {
            "TEAM": "A group of people, each with individual authorisations, assigned responsibility for specified resources.",
            "PROJECT": "A research initiative.",
            "COLLECTION": "A collection of one or more diverse research datasets which are to be unified according to a defined schema.",
            "DATASET": "A series of data sources that are otherwise identical except for temporal differences",
            "DATA": "A data source",
            "SCHEMA": "A specified set of terms which define source data structure and validation.",
            "METHOD": "A list of consecutive instructions which unambiguously restructure source data to validate against a specified schema.",
        }
        return description[self.value]

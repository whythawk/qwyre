from enum import Enum


class CurrencyType(str, Enum):
    USD = "usd"
    GBP = "gbp"
    EUR = "eur"

    def describe(self):
        description = {"usd": "$", "gbp": "£", "eur": "€"}
        return description[self.value]

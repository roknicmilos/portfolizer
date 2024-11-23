from dataclasses import dataclass
from datetime import date

from apps.portfolio.models import Address


@dataclass
class PersonalDetails:
    address_label: str | None
    address_link: str | None
    birthday: date | None

    @property
    def address(self) -> Address | None:
        if self.address_label:
            return Address(self.address_label, self.address_link)
        return None

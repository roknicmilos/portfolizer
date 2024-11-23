from dataclasses import dataclass


@dataclass
class Contact:
    email: str | None
    phone: str | None

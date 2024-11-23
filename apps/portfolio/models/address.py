from dataclasses import dataclass


@dataclass
class Address:
    label: str
    link: str | None

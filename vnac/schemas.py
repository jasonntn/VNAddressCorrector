import re
from typing import Optional

from pydantic import BaseModel, field_validator

from vnac.utils import clean_str


class Division(BaseModel):
    name: str
    code: Optional[str] = None

    @field_validator("name", mode="before")
    @classmethod
    def clean(cls, v):
        return clean_str(v)


class Address(BaseModel):
    country: Optional[Division] = None
    province: Optional[Division] = None
    district: Optional[Division] = None
    ward: Optional[Division] = None
    street: Optional[Division] = None

    @classmethod
    def from_str(cls, s: str) -> "Address":
        """Create Address instance from string

        Args:
            s (str): address string

        Returns:
            Address: address instance
        """
        parts = clean_str(s).rsplit(",", 3)
        match = re.findall("(việt\s*nam)", parts[-1], re.I)
        country = Division(name=match[0]) if bool(match) else None
        province = Division(name=parts[-1])
        district = Division(name=parts[-2]) if len(parts) > 1 else None
        ward = Division(name=parts[-3]) if len(parts) > 2 else None
        street = Division(name=parts[-4]) if len(parts) > 3 else None
        return cls(country=country, province=province, district=district, ward=ward, street=street)

    def __str__(self) -> str:
        return ", ".join([i.name for i in [self.street, self.ward, self.district, self.province, self.country] if i])

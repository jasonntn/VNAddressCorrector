import re
from dataclasses import dataclass

from vnac.utils import clean_str


@dataclass
class Division:
    name: str = None
    code: str = None


@dataclass
class Address:
    country: Division = None
    province: Division = None
    district: Division = None
    ward: Division = None
    street: Division = None

    @classmethod
    def from_str(cls, s: str) -> "Address":
        """Create Address instance from string

        Args:
            s (str): address string

        Returns:
            Address: address instance
        """
        parts = clean_str(s).rsplit(",", 3)
        match = re.findall("(việt\\s*nam)", parts[-1], re.I)
        country = Division(name=clean_str(match[0])) if bool(match) else None
        province = Division(name=clean_str(parts[-1]))
        district = Division(name=clean_str(parts[-2])) if len(parts) > 1 else None
        ward = Division(name=clean_str(parts[-3])) if len(parts) > 2 else None
        street = Division(name=clean_str(parts[-4])) if len(parts) > 3 else None
        return cls(country=country, province=province, district=district, ward=ward, street=street)

    def __str__(self) -> str:
        return ", ".join([i.name for i in [self.street, self.ward, self.district, self.province, self.country] if i])

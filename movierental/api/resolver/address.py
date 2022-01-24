""" Resolver for address """

from typing import List, Optional

from movierental.api.definition import Address, City
from movierental.database.dataaccess import address


async def get_address(
    root: Address,
    address_ids: Optional[List[int]] = None,
    districts: Optional[List[str]] = None,
    limit: int = 10,
) -> List[Address]:
    addresses = address.get_address(
        address_ids=address_ids, districts=districts, limit=limit
    )
    return [Address.from_instance(an_address) for an_address in addresses]


async def get_city(root: City, limit: int = 10) -> List[City]:
    cities = address.get_city(limit)

    return [City.from_instance(city) for city in cities]

""" Resolver for customer """

from typing import List, Optional

from movierental.api.definition import Customer
from movierental.database.dataaccess import customer


async def get_customer(
    limit: int = 10,
    city: Optional[str] = None,
    active: Optional[bool] = None,
) -> List[Customer]:
    customers = customer.get_customer(limit=limit, city=city, active=active)
    return [Customer.from_instance(a_customer) for a_customer in customers]

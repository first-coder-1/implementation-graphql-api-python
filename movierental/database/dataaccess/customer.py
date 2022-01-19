""" Methods for fetching film related data from database """

import asyncio
import sqlalchemy
from sqlalchemy.orm import joinedload
from movierental.database.models import Customer, Addres, Store, City, Country
from .db import db, session


def get_customer(limit=None, city=None, active=None):
    query = (
        session.query(Customer)
        .options(
            joinedload(Customer.address)
            .joinedload(Addres.city)
            .joinedload(City.country)
        )
        .options(joinedload(Customer.store))
    )

    query = (
        session.query(Customer)
        .join(Customer.address)
        .join(Addres.city)
        .join(City.country)
        .join(Customer.store)
    )

    if city is not None:
        query = query.filter(City.city == city)

    if active is not None:
        active_flag = 1 if active is True else 0
        query = query.filter(Customer.active == active_flag)

    query = query.limit(limit)

    return query


if __name__ == "__main__":
    get_customer(5)
    # asyncio.run(get_actor(5))

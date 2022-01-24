""" Methods for fetching film related data from database """

import asyncio

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from movierental.database.models import Addres, City, Country

from .db import db, session


async def get_address_s(limit=None):
    await db.connect()
    query = (
        select(Addres)
        .options(joinedload(Addres.city).joinedload(City.country))
        .limit(limit)
    )
    address = await db.fetch_all(query)

    return address


def get_address(address_ids=None, districts=None, limit=None):
    query = (
        session.query(Addres)
        .options(joinedload(Addres.city).joinedload(City.country))
        .limit(limit)
    )

    if address_ids:
        query = query.filter(Addres.address_id.in_(address_ids))

    if districts:
        query = query.filter(Addres.district.in_(districts))

    query = query.limit(limit)

    return query


def get_city(limit=None):
    query = session.query(City).options(joinedload(City.country)).limit(limit)

    return query


if __name__ == "__main__":
    get_address(5)
    # asyncio.run(get_address_s(5))

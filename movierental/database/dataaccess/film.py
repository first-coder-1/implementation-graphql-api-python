""" Methods for fetching film related data from database """

import asyncio
import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from movierental.database.models import Film, FilmActor, Actor
from .db import db, session


async def get_film(film_ids=None, limit=10):
    query = session.query(Film).options(joinedload(Film.language))

    if film_ids:
        query = query.filter(Film.film_id.in_(film_ids))

    query = query.limit(limit)

    return query


async def get_actors_for_a_film(film_id):
    query = session.select(FilmActor).filter(FilmActor.film_id == film_id)

    actor_ids = []
    for actor in query:
        actor_ids.append(actor.actor_id)

    return actor_ids


if __name__ == "__main__":
    asyncio.run(get_film())

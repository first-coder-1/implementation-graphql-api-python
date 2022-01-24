""" Methods for fetching film related data from database """

import asyncio

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from strawberry.dataloader import DataLoader
from strawberry.extensions import Extension

from movierental.database.models import Actor, Film, FilmActor

from .db import db, session


async def get_actors(limit=10):
    query = session.query(Actor)

    query = query.limit(limit)

    return query


async def get_actor_by_id(actor_ids=None):
    query = session.query(Actor)

    if actor_ids:
        query = query.filter(Actor.actor_id.in_(actor_ids))

    return query


def get_films_for_actor(actor_id: int):
    query = session.query(FilmActor).filter(FilmActor.actor_id == actor_id)

    film_ids = []
    for film in query:
        film_ids.append(film.film_id)

    return film_ids


def add_new_actor(first_name: str, last_name: str) -> Actor:
    actor = Actor()
    actor.first_name = first_name
    actor.last_name = last_name

    session.add(actor)
    session.commit()

    return actor


if __name__ == "__main__":
    get_actors(5)
    # asyncio.run(get_actor(5))

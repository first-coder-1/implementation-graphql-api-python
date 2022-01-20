""" Methods for fetching film related data from database """

import asyncio
import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from movierental.database.models import Film, FilmActor, Actor
from .db import db, session

from strawberry.dataloader import DataLoader
from strawberry.extensions import Extension


async def get_actor_s(limit=None):
    await db.connect()
    query = (
        select(Actor, FilmActor, Film)
        .filter(Actor.actor_id == FilmActor.actor_id)
        .filter(FilmActor.film_id == Film.film_id)
        .limit(limit)
    )
    actors = await db.fetch_all(query)

    print(len(actors))

    for actor in actors:
        for val in actor.items():
            print(val)

    return actors


async def get_actor(actor_ids=None, limit=None):
    query = session.query(Actor)

    if actor_ids:
        query = query.filter(Actor.actor_id.in_(actor_ids))

    query = query.limit(limit)

    print(f"******************************Database called here, {actor_ids}")
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


class DataLoaderExtension(Extension):
    def on_request_start(self):
        self.execution_context.context["actor_loader"] = DataLoader(get_actor)


if __name__ == "__main__":
    get_actor(5)
    # asyncio.run(get_actor(5))

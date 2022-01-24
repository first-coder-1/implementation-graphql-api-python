from __future__ import annotations
import typing
from typing import List, Optional

import strawberry
from strawberry.types import Info

import movierental.database.dataaccess.actor as ActorDA
import movierental.database.dataaccess.film as FilmDA
from movierental.database.dataloader import DataLoaders


@strawberry.type(description="An actor and it's attributes")
class Actor:
    actor_id: int = strawberry.field(description="Id of the actor")
    first_name: str = strawberry.field(description="First name of the actor")
    last_name: str = strawberry.field(description="Last name of the actor")

    @strawberry.field(description="films for the actor")
    async def film(
        self, info: Info
    ) -> Optional[List[strawberry.LazyType["Film", "movierental.api.definition.film"]]]:
        from movierental.api.definition.film import Film

        film_ids = ActorDA.get_films_for_actor(self.actor_id)
        films = await info.context[DataLoaders.load_films].load_many(film_ids)
        return [Film.from_instance(a_film) for a_film in films]

    @classmethod
    def from_instance(cls, instance):
        return cls(
            actor_id=instance.actor_id,
            first_name=instance.first_name,
            last_name=instance.last_name,
        )

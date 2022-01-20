from __future__ import annotations
import strawberry
import typing
from typing import Optional, List


import movierental.database.dataaccess.film as FilmDA
import movierental.database.dataaccess.actor as ActorDA


@strawberry.type(description="An actor and it's attributes")
class Actor:
    actor_id: int = strawberry.field(description="Id of the actor")
    first_name: str = strawberry.field(description="First name of the actor")
    last_name: str = strawberry.field(description="Last name of the actor")

    @strawberry.field(description="films for the actor")
    async def film(
        self,
    ) -> Optional[
        List[strawberry.LazyType["Film", "movierental.api.definitions.film"]]
    ]:
        from movierental.api.definitions.film import Film

        film_ids = ActorDA.get_films_for_actor(self.actor_id)
        return [
            Film.from_instance(a_film)
            for a_film in await FilmDA.get_film(film_ids=film_ids)
        ]

    @classmethod
    def from_instance(cls, instance):
        print(instance)
        print(type(instance))
        return cls(
            actor_id=instance.actor_id,
            first_name=instance.first_name,
            last_name=instance.last_name,
        )

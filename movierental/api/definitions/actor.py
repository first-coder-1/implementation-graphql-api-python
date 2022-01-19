import strawberry
from typing import Optional, List

from movierental.api.definitions.film import Film
from movierental.database.models import Actor as ActorModel
from movierental.database.models import Film as FilmModel
import movierental.database.dataaccess.film as FilmDA
import movierental.database.dataaccess.actor as ActorDA


@strawberry.type(description="An actor and it's attributes")
class Actor:
    actor_id: int = strawberry.field(description="Id of the actor")
    first_name: str = strawberry.field(description="First name of the actor")
    last_name: str = strawberry.field(description="Last name of the actor")

    @strawberry.field(description="Films of the actor")
    def film(self) -> Optional[List[Film]]:
        film_ids = ActorDA.get_films_for_actor(self.actor_id)
        return FilmDA.get_film(film_ids=film_ids)

    @classmethod
    def from_instance(cls, instance):
        return cls(
            actor_id=instance.actor_id,
            first_name=instance.first_name,
            last_name=instance.last_name,
        )

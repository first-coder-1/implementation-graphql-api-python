""" Module for defining schema of strawberry graphql """
from typing import List
from typing import Optional
import strawberry

from movierental.database.dataaccess import film as FilmDA
from movierental.database.dataaccess import actor as ActorDA
from movierental.database.dataaccess import address as AddressDA
from movierental.database.dataaccess import customer as CustomerDA
from movierental.api.definitions.film import Film
from movierental.api.definitions.actor import Actor
from movierental.api.definitions.address import Address
from movierental.api.definitions.customer import Customer
from movierental.database.models import Actor as ActorModel


@strawberry.type
class Query:
    @strawberry.field(description="Get details of a film")
    async def film(
        self, film_ids: Optional[List[int]] = None, limit: int = 10
    ) -> List[Film]:
        films = await FilmDA.get_film(film_ids=film_ids, limit=limit)
        films = [Film.from_instance(a_film) for a_film in films]

        return films

    @strawberry.field(description="Get details of an actor")
    async def actor(
        self, actor_ids: Optional[List[int]] = None, limit: int = 10
    ) -> List[Actor]:
        actors = ActorDA.get_actor(actor_ids=actor_ids, limit=limit)

        actors = [Actor.from_instance(an_actor) for an_actor in actors]

        for actor in actors:
            film_ids = ActorDA.get_films_for_actor(actor.actor_id)
            actor.film = FilmDA.get_film(film_ids)

        return actors

    @strawberry.field(description="Get details of address")
    async def address(self, limit: int = 10) -> List[Address]:
        addresses = AddressDA.get_address(limit=limit)
        return [Address.from_instance(an_address) for an_address in addresses]

    @strawberry.field(description="Get details of customer")
    async def customer(
        self, limit: int = 10, city: Optional[str] = None, active: Optional[bool] = None
    ) -> List[Customer]:
        customer = CustomerDA.get_customer(limit=limit, city=city, active=active)
        return [Customer.from_instance(a_customer) for a_customer in customer]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def actor(self, first_name: str, last_name: str) -> Actor:
        return ActorDA.add_new_actor(first_name=first_name, last_name=last_name)


schema = strawberry.Schema(query=Query, mutation=Mutation)

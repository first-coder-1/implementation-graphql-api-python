""" Module for defining schema of strawberry graphql """
from typing import List
from typing import Optional
import strawberry
from strawberry.types import Info
from strawberry.dataloader import DataLoader
from strawberry.extensions import Extension

from movierental.database.dataaccess import film as FilmDA
from movierental.database.dataaccess import actor as ActorDA
from movierental.database.dataaccess import address as AddressDA
from movierental.database.dataaccess import customer as CustomerDA
from movierental.api.definitions.film import Film
from movierental.api.definitions.actor import Actor
from movierental.api.definitions.address import Address, City
from movierental.api.definitions.customer import Customer
from movierental.database.models import Actor as ActorModel
import movierental.database.dataloader as dataloader


# actor_loader = DataLoader(load_fn=ActorDA.get_actor)


@strawberry.type
class Query:
    @strawberry.field(description="Get details of a film")
    async def film(
        self,
        info: Info,
        film_ids: Optional[List[int]] = None,
    ) -> List[Film]:
        films = await info.context[dataloader.DataLoaders.load_films].load_many(
            film_ids
        )
        films = [Film.from_instance(a_film) for a_film in films]

        return films

    @strawberry.field(description="Get details of an actor")
    async def actor(
        self,
        info: Info,
        actor_ids: Optional[List[int]] = None,
    ) -> List[Actor]:
        actors = await info.context[dataloader.DataLoaders.load_actor].load_many(
            actor_ids
        )

        actors = [Actor.from_instance(an_actor) for an_actor in actors]

        return actors

    @strawberry.field(description="Get details of address")
    async def address(
        self,
        address_ids: Optional[List[int]] = None,
        districts: Optional[List[str]] = None,
        limit: int = 10,
    ) -> List[Address]:
        addresses = AddressDA.get_address(
            address_ids=address_ids, districts=districts, limit=limit
        )
        return [Address.from_instance(an_address) for an_address in addresses]

    @strawberry.field(description="Get details of city")
    async def city(self, limit: int = 10) -> List[City]:
        cities = AddressDA.get_city(limit)

        return [City.from_instance(city) for city in cities]

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


schema = strawberry.Schema(
    query=Query, mutation=Mutation, extensions=(dataloader.DataLoadersExtension,)
)

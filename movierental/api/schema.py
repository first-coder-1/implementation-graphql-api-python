""" Module for defining schema of strawberry graphql """

from typing import List

import strawberry

from movierental.database import dataloader
from movierental.database.dataaccess import actor as ActorDA

from .definition import Actor, Address, City, Customer, Film
from .resolver import (
    actor as actor_resolver,
    address as address_resolver,
    customer as customer_resolver,
    film as film_resolver,
)


@strawberry.type
class Query:

    film: List[Film] = strawberry.field(
        resolver=film_resolver.get_film, description="Details for an film"
    )

    actor: List[Actor] = strawberry.field(
        resolver=actor_resolver.get_actor, description="Details for an actor"
    )

    address: List[Address] = strawberry.field(
        resolver=address_resolver.get_address, description="Get details of an address"
    )

    city: List[City] = strawberry.field(
        resolver=address_resolver.get_city, description="Get details of a city"
    )

    customer: List[Customer] = strawberry.field(
        resolver=customer_resolver.get_customer, description="Get details of a customer"
    )


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def actor(self, first_name: str, last_name: str) -> Actor:
        return ActorDA.add_new_actor(first_name=first_name, last_name=last_name)


schema = strawberry.Schema(
    query=Query, mutation=Mutation, extensions=(dataloader.DataLoadersExtension,)
)

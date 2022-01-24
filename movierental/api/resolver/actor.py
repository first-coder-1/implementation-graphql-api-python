""" Defining resolvers for actor """

from typing import List, Optional

from strawberry.types import Info

from movierental.api.definition import Actor
from movierental.database.dataaccess import actor
from movierental.database.dataloader import DataLoaders


async def get_actor(
    info: Info,
    actor_ids: Optional[List[int]] = None,
) -> List[Actor]:
    """Resolver for actor object"""

    if actor_ids:
        actors = await info.context[DataLoaders.load_actor].load_many(actor_ids)
    else:
        actors = await actor.get_actors()

    actors = [Actor.from_instance(an_actor) for an_actor in actors]

    return actors

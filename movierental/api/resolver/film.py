""" Defining resolvers for film"""

from typing import List, Optional

from strawberry.types import Info

from movierental.api.definition import Film
from movierental.database.dataloader import DataLoaders


async def get_film(
    info: Info,
    film_ids: Optional[List[int]] = None,
) -> List[Film]:
    films = await info.context[DataLoaders.load_films].load_many(film_ids)
    films = [Film.from_instance(a_film) for a_film in films]

    return films

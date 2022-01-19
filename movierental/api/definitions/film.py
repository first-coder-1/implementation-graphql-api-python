import strawberry
from typing import List, Optional

from movierental.database.models import Film as FilmModel


@strawberry.type(description="A film and it's attributes")
class Film:
    film_id: int
    title: str
    description: str
    release_year: int
    language: str
    original_language: int
    rental_duration: int
    rental_rate: float
    length: int
    replacement_cost: float
    mpaa_rating: str

    @classmethod
    def from_instance(cls, instance):
        return cls(
            film_id=instance.film_id,
            title=instance.title,
            description=instance.description,
            release_year=instance.release_year,
            language=instance.language.language,
            original_language=instance.original_language,
            rental_duration=instance.rental_duration,
            rental_rate=instance.rental_rate,
            length=instance.length,
            replacement_cost=instance.replacement_cost,
            mpaa_rating=instance.mpaa_rating,
        )

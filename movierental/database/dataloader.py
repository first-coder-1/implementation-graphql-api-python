import enum

from strawberry.dataloader import DataLoader
from strawberry.extensions import Extension

import movierental.database.dataaccess as dataaccess


class DataLoaders(enum.Enum):
    load_actor = enum.auto()
    load_films = enum.auto()


class DataLoadersExtension(Extension):
    def on_request_start(self):
        print("^^^^^^^^^^^^^^^^^^^^This was run^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        self.execution_context.context.update(
            {
                DataLoaders.load_actor: DataLoader(dataaccess.actor.get_actor),
                DataLoaders.load_films: DataLoader(dataaccess.film.get_film),
            }
        )

""" Module for initializing FastAPI app object """


from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from movierental.api.schema import schema


graphql_app = GraphQLRouter(schema)


app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

# implementation-graphql-api-python

This is an application to demonstrate implementation of GraphQL API backend in Python.


# Components

- [FastAPI](https://github.com/tiangolo/fastapi) is used as a flexible web framework
- [Strawberry](https://github.com/strawberry-graphql/strawberry) is used for GraphQL integration
- [PostgreSQL](https://www.postgresql.org/) is used for database
- [Pagila](https://github.com/devrimgunduz/pagila) (fictional movie rental store) dataset is used as sample application data in database
- [SQL Alchemy](https://github.com/sqlalchemy/sqlalchemy) is used as an ORM to connect to the DB
- [Poetry](https://github.com/python-poetry/poetry) is used for Python dependency management


# Features

- Dataloaders implemented for some objects


# Scope of Improvement

- Pagination
- Nested filters
- Authentication
- Query nesting level limit
- Query execution time limit
- Limit on max number of objects in a query result
- Asynchronous database access

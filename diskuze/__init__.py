from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from diskuze.dependencies.context import AppContext
from diskuze.schema import schema

app = FastAPI()

graphql_app = GraphQLRouter(schema, context_getter=AppContext)
app.include_router(graphql_app, prefix="/graphql")

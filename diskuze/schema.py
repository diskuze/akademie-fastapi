from typing import Any
from typing import List
from typing import Optional

import strawberry
from sqlalchemy import select
from sqlalchemy.sql.functions import count
from strawberry.types import Info

from diskuze.dependencies.context import AppContext
from diskuze import models


# TODO: task 01: define GraphQL type for discussion model here
#  https://strawberry.rocks/docs/general/schema-basics
@strawberry.type
class Discussion:
    ...

# TODO: task 03: define GraphQL types for the rest of the models from `diskuze.models` module
#  https://strawberry.rocks/docs/general/schema-basics

# TODO: task 04: define relationships Comment.user, Comment.discussion, Comment.replyTo
#  https://strawberry.rocks/docs/guides/dataloaders


@strawberry.type
class Query:
    @strawberry.field(description="Says \"Hello World!\"")
    def hello(self) -> str:
        return "Hello World!"

    @strawberry.field(description="Gives boring statistics about comments total")
    async def total(self, info: Info[AppContext, Any]) -> int:
        async with info.context.db.session() as session:
            query = select(count()).select_from(models.Comment)
            result = await session.execute(query)
            total = result.scalar()

        return total

    # TODO: task 02: define endpoint to get a discussion from
    #  https://strawberry.rocks/docs/general/queries


@strawberry.input
class CommentInput:
    content: str
    discussion_canonical: str
    reply_to: Optional[int] = None


@strawberry.type
class CommentOutput:
    comment: Optional["Comment"] = None


@strawberry.type
class Mutation:
    # TODO: task 06: define mutation `createComment`
    #  https://strawberry.rocks/docs/general/mutations
    @strawberry.mutation
    async def create_comment(
            self,
            info: Info[AppContext, Any],
            input_: strawberry.arguments.Annotated[CommentInput, strawberry.argument(name="input")],
    ) -> CommentOutput:
        # TODO: check input data
        ...

        # TODO: create the comment in database
        ...

        return CommentOutput(comment=None)


schema = strawberry.Schema(Query, Mutation)

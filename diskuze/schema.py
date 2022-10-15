import asyncio
from typing import Any
from typing import List
from typing import Optional

import strawberry
from sqlalchemy import select, exists
from sqlalchemy.sql.functions import count
from strawberry.types import Info

from diskuze.dependencies.context import AppContext
from diskuze import models


# TODO: task 01: define GraphQL type for discussion model here
#  https://strawberry.rocks/docs/general/schema-basics
@strawberry.type
class Discussion:
    id: int
    canonical: str

    @staticmethod
    def from_model(discussion: models.Discussion) -> "Discussion":
        return Discussion(id=discussion.id, canonical=discussion.canonical)

    @strawberry.field
    async def comments(
            self,
            info: Info[AppContext, Any],
            first: int = 10,
            offset: int = 0,
    ) -> List["Comment"]:
        async with info.context.db.session() as session:
            query = (
                select(models.Comment)
                .where(models.Comment.discussion_id == self.id)
                .limit(first)
                .offset(offset)
            )
            result = await session.execute(query)
            comments = result.scalars()

        return [Comment.from_model(comment) for comment in comments]


# TODO: task 03: define GraphQL types for the rest of the models from `diskuze.models` module
#  https://strawberry.rocks/docs/general/schema-basics
@strawberry.type
class User:
    id: int
    nick: str


@strawberry.type
class Comment:
    id: int
    content: str

    user_id: strawberry.Private[int]
    discussion_id: strawberry.Private[int]
    reply_to_id: strawberry.Private[int]

    @staticmethod
    def from_model(comment: models.Comment) -> "Comment":
        return Comment(
            id=comment.id,
            content=comment.content,
            discussion_id=comment.discussion_id,
            user_id=comment.user_id,
            reply_to_id=comment.reply_to_id,
        )

    # TODO: task 04: define relationships Comment.user, Comment.discussion, Comment.replyTo
    #  https://strawberry.rocks/docs/guides/dataloaders
    @strawberry.field
    async def user(self, info: Info[AppContext, Any]) -> User:
        user = await info.context.data_loader.user.load(self.user_id)
        return User(
            id=user.id,
            nick=user.nick,
        )

    @strawberry.field
    async def discussion(self, info: Info[AppContext, Any]) -> Discussion:
        discussion = await info.context.data_loader.discussion.load(self.discussion_id)
        return Discussion.from_model(discussion)

    @strawberry.field
    async def reply_to(self, info: Info[AppContext, Any]) -> Optional["Comment"]:
        if not self.reply_to_id:
            return None

        comment = await info.context.data_loader.comment.load(self.reply_to_id)
        return Comment.from_model(comment)

    @strawberry.field
    async def replies(
            self,
            info: Info[AppContext, Any],
            first: int = 10,
            offset: int = 0,
    ) -> List["Comment"]:
        async with info.context.db.session() as session:
            query = (
                select(models.Comment)
                .where(models.Comment.reply_to_id == self.id)
                .limit(first)
                .offset(offset)
            )
            result = await session.execute(query)
            comments = result.scalars()

        return [Comment.from_model(comment) for comment in comments]

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
    @strawberry.field(description="Gets a discussion by its canonical")
    async def discussion(
            self,
            info: Info[AppContext, Any],
            canonical: str,
    ) -> Optional[Discussion]:
        async with info.context.db.session() as session:
            query = (
                select(models.Discussion)
                .where(models.Discussion.canonical == canonical)
            )
            result = await session.execute(query)
            discussion = result.scalar()

        if not discussion:
            return None

        return Discussion.from_model(discussion)

    @strawberry.field(description="Gets a comment by its id")
    async def comment(
            self,
            info: Info[AppContext, Any],
            id_: strawberry.arguments.Annotated[int, strawberry.argument(name="id")],
    ) -> Optional[Comment]:
        async with info.context.db.session() as session:
            query = (
                select(models.Comment)
                .where(models.Comment.id == id_)
            )
            result = await session.execute(query)
            comment = result.scalar()

        if not comment:
            return None

        return Comment.from_model(comment)


@strawberry.input
class CommentInput:
    content: str
    discussion_canonical: str
    reply_to: Optional[int] = None


@strawberry.type
class CommentOutput:
    comment: Optional[Comment] = None
    error: Optional[str] = None


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
        if not input_.content:
            return CommentOutput(error="please, provide content")

        if not info.context.auth_user:
            return CommentOutput(error="please, authorize")

        # TODO: create the comment in database
        async with info.context.db.session() as session:
            query = (
                select(models.Discussion.id)
                .where(models.Discussion.canonical == input_.discussion_canonical)
            )
            result = await session.execute(query)
            discussion_id = result.scalar()

            if not discussion_id:
                return CommentOutput(error="discussion does not exist")

            if input_.reply_to is not None:
                query = select(
                    exists(
                        select(1)
                        .select_from(models.Comment)
                        .where(models.Comment.id == input_.reply_to)
                    )
                )
                result = await session.execute(query)
                reply_exists = result.scalar()

                if not reply_exists:
                    return CommentOutput(error="reply does not exist")

            comment = models.Comment(
                content=input_.content,
                discussion_id=discussion_id,
                reply_to_id=input_.reply_to,
                user_id=info.context.auth_user.id,
            )
            session.add(comment)

        return CommentOutput(comment=Comment.from_model(comment))


schema = strawberry.Schema(Query, Mutation)

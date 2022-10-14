import asyncio
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

import httpx
from fastapi import Depends
from httpx import Response
from sqlalchemy import select
from strawberry.dataloader import DataLoader

from diskuze.models import User
from diskuze.dependencies.database import Database
from diskuze.dependencies.database import get_database
from diskuze.models import Base
from diskuze.models import Comment
from diskuze.models import Discussion

# Implementations of Strawberry's DataLoader
# https://strawberry.rocks/docs/guides/dataloaders

T = TypeVar("T", bound=Base)


class DatabaseIdentityDataLoader:
    """
    Common data loader to load items from database by its identity key
    """

    def __init__(self, db: Database, model: Type[T]):
        self.db = db
        self.model = model

    async def load(self, ids: List[int]) -> List[T]:
        async with self.db.session() as session:
            query = select(self.model).where(self.model.id.in_(ids))
            result = await session.execute(query)
            items = result.scalars().all()

        return items


# TODO: task 08: implement data loader to get user's name from external service
#   https://strawberry.rocks/docs/guides/dataloaders
#   https://github.com/encode/httpx

# async def load_full_name(...) -> List[Optional[str]]: ...


class DataLoaderRegistry:
    """
    Collection of available data loaders
    """

    def __init__(self, db: Database = Depends(get_database)):
        self.comment = DataLoader(load_fn=DatabaseIdentityDataLoader(db, Comment).load)
        self.discussion = DataLoader(load_fn=DatabaseIdentityDataLoader(db, Discussion).load)
        self.user = DataLoader(load_fn=DatabaseIdentityDataLoader(db, User).load)
        # TODO: task 08: add the name loader to registry to access it properly

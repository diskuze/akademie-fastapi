from typing import Optional

from fastapi import Depends
from fastapi import Request
from fastapi import Header
from sqlalchemy import select

from diskuze.models import User
from diskuze.dependencies.database import Database
from diskuze.dependencies.database import get_database


# TODO: task 07: implement authentication process
#  https://fastapi.tiangolo.com/tutorial/header-params/
#  https://fastapi.tiangolo.com/advanced/using-request-directly/

async def get_auth_user(
        # TODO: what dependencies do we need?
        request: Request,
        db: Database = Depends(get_database),
        authorization: str = Header(default=""),
) -> Optional[User]:
    """
    Gets currently authorized user based on Request headers and return that.
    Otherwise, return None.

    The header should come in the form of:
    Authorization: User <nick>
    """

    # authorization = request.headers.get("authorization") or ""
    authorization_split = authorization.split(" ", 1)

    if len(authorization_split) != 2:
        return None  # unauthorized or invalid format

    auth_type, nick = authorization_split
    if auth_type != "User" or not nick:
        return None  # invalid type or empty nick

    async with db.session() as session:
        query = select(User).where(User.nick == nick)
        result = await session.execute(query)
        user = result.scalar()

    return user

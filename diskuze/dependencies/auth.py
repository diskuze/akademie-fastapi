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
) -> Optional[User]:
    """
    Gets currently authorized user based on Request headers and return that.
    Otherwise, return None.

    The header should come in the form of:
    Authorization: User <nick>
    """
    ...

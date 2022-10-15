from typing import Optional

from fastapi import Depends
from strawberry.fastapi import BaseContext

from diskuze.dependencies.config import get_config
from diskuze.models import User
from diskuze.dependencies.auth import get_auth_user
from diskuze.dependencies.config import Config
from diskuze.dependencies.data_load import DataLoaderRegistry
from diskuze.dependencies.database import Database
from diskuze.dependencies.database import get_database


class AppContext(BaseContext):
    """
    Custom typed context class
    https://strawberry.rocks/docs/integrations/fastapi#context_getter
    """

    def __init__(
        self,
        config: Config = Depends(get_config),
        db: Database = Depends(get_database),
        data_loader: DataLoaderRegistry = Depends(DataLoaderRegistry),
        auth_user: Optional[User] = Depends(get_auth_user),
    ):
        super().__init__()
        self.config = config
        self.db = db
        self.data_loader = data_loader
        # TODO: task 07: add authenticated user dependency to context
        self.auth_user = auth_user

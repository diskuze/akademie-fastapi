from pydantic import BaseSettings
from pydantic.tools import lru_cache


class Config(BaseSettings):
    DB_HOST = "temp-it-akademie.cms8yp1jph9y.eu-central-1.rds.amazonaws.com"
    DB_USER = "temp_it_akademie"
    DB_PASS = "itAkadem1e"
    DB_NAME = "temp_it_akademie"


@lru_cache()
def get_config():
    """
    Cached configuration factory
    For details, see https://fastapi.tiangolo.com/advanced/settings/#lru_cache-technical-details
    """
    return Config()

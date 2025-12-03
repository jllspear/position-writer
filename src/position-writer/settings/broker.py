from pydantic_settings import BaseSettings


class BrokerSettings(BaseSettings):
    url: str
    port: int
    username: str
    password: str
    topics: dict[str, str]
    first_reconnect_delay: int = 1
    reconnect_rate: int = 2
    max_reconnect_count: int = 8
    max_reconnect_delay: int = 180
    recheck_equipment_interval: int = 180
    verbose: bool = False

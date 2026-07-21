from utils.api_wrapper.clients import BaseAPIClient


class SteamPlayerCountClient(BaseAPIClient):
    def __init__(self, logger, base_url: str):
        super().__init__(
            base_url=base_url,
            logger=logger,
            rate_limit_delay=1
        )

    async def get_steam_count(self) -> dict:
        return await self.get(
            endpoint="",
            params={"appid": 553850},
        )


class SteamNewsClient(BaseAPIClient):
    def __init__(self, logger, base_url: str):
        super().__init__(
            base_url=base_url,
            logger=logger,
            rate_limit_delay=1
        )

    async def get_steam_news(self) -> dict:
        return await self.get(
            endpoint="",
        )

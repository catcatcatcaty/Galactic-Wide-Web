from utils.api_wrapper.clients import BaseAPIClient


class SteamPlayerCountClient(BaseAPIClient):
    def __init__(self, logger, base_url: str):
        super().__init__(
            base_url=base_url,
            logger=logger,
        )

    async def get_steam_count(self) -> dict[str, dict[str, int]] | None:
        return await self.get()


class SteamNewsClient(BaseAPIClient):
    def __init__(self, logger, base_url: str):
        super().__init__(
            base_url=base_url,
            logger=logger,
        )

    async def get_steam_news(self) -> dict | None:
        return await self.get()

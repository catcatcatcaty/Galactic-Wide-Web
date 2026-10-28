from utils.api_wrapper.clients import BaseAPIClient
from utils.dataclasses import Config


class AuthedClient(BaseAPIClient):
    def __init__(self, logger):
        super().__init__(
            base_url=Config.AUTHED_API_URL,
            logger=logger,
            headers=Config.AUTHED_API_HEADERS,
        )

    async def get_dss_votes(self) -> dict | None:
        return await self.get("/raw/election")

    async def get_personal_order(self) -> dict | None:
        return await self.get("/raw/assignment")


class AltDSSVotesAuthedClient(BaseAPIClient):
    def __init__(self, logger):
        super().__init__(
            base_url=Config.ALT_AUTHED_API_DSS_ENDPOINT,
            logger=logger,
            headers=Config.ALT_AUTHED_API_HEADERS,
        )

    async def get_space_stations_votes(
        self, war_id: int, period_id: str
    ) -> dict | None:
        return await self.get(f"/{war_id}/{period_id}")


class AltPOAuthedClient(BaseAPIClient):
    def __init__(self, logger):
        super().__init__(
            base_url=Config.ALT_PO_ENDPOINT,
            logger=logger,
            headers=Config.ALT_AUTHED_API_HEADERS,
        )

    async def get_personal_order(self) -> dict | None:
        return await self.get()


class AltSuperstoreAuthedClient(BaseAPIClient):
    def __init__(self, logger):
        super().__init__(
            base_url=Config.ALT_SUPERSTORE_ENDPOINT,
            logger=logger,
            headers=Config.ALT_AUTHED_API_HEADERS,
        )

    async def get_superstore(self) -> dict | None:
        return await self.get()

    async def get_rotating(self) -> dict | None:
        return await self.get("/rotation")


class AltWarbondsAuthedClient(BaseAPIClient):
    def __init__(self, logger):
        super().__init__(
            base_url=Config.ALT_WARBONDS_ENDPOINT,
            logger=logger,
            headers=Config.ALT_AUTHED_API_HEADERS,
        )

    async def get_warbonds_index(self) -> list[dict] | None:
        return await self.get()

    async def get_with_id(self, warbond_id: int) -> dict | None:
        return await self.get(f"/{warbond_id}")

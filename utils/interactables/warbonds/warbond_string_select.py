from disnake import SelectOption
from disnake.ui import StringSelect
from utils.api_wrapper.models import Warbond


class WarbondsStringSelect(StringSelect):
    def __init__(self, index, warbonds: list[Warbond]):
        super().__init__(
            placeholder=(
                f"Warbonds {((index + 1) * 25) - 24}-{(index * 25) + len(warbonds)}"
                if len(warbonds) > 1
                else f"Warbond {(index * 25) + 1}"
            ),
            min_values=1,
            max_values=1,
            options=[
                SelectOption(
                    label=warbond.name,
                    value=warbond.id,
                    description=f"{len(warbond.pages)} Pages - {len([i for p in warbond.pages for i in p.items])} items - total cost {sum([i.cost for p in warbond.pages for i in p.items])} Medals",
                )
                for warbond in warbonds
            ],
            custom_id=f"warbond_dropdown_{index}",
        )

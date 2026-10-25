from datetime import datetime, timedelta, timezone
from utils.api_wrapper.models.endpoint_items import EndpointItem
from utils.dataclasses import Faction, Factions
from utils.dataclasses.enums import AssignmentTaskType
from utils.functions import arrowhead_format, health_bar
from utils.trackers import BaseTrackerEntry


class Assignment:
    def __init__(
        self,
        raw_assignment_data: dict,
        war_start_timestamp: int,
        endpoint_items: dict[int, EndpointItem],
    ) -> None:
        """Organised data of an Assignment or Major Order"""
        self.id: int = raw_assignment_data["id32"]
        self.title: str = raw_assignment_data["setting"].get("overrideTitle", None)
        self.briefing: str = arrowhead_format(
            raw_assignment_data["setting"].get("overrideBrief", None)
            if raw_assignment_data["setting"].get("overrideBrief", None)
            not in ([], None)
            else ""
        )
        self.description: str = (
            raw_assignment_data["setting"].get("taskDescription", None)
            if raw_assignment_data["setting"].get("taskDescription", None)
            not in ([], None, raw_assignment_data["setting"].get("overrideBrief", None))
            else ""
        )
        self.tasks: list[Assignment.Task] = []
        for index, task in enumerate(iterable=raw_assignment_data["setting"]["tasks"]):
            self.tasks.append(
                Assignment.Task(
                    task=task, current_progress=raw_assignment_data["progress"][index]
                )
            )
        self.rewards: list[Assignment.Reward] = [
            Assignment.Reward(i, endpoint_items)
            for i in raw_assignment_data["setting"]["rewards"]
        ]
        self.starts_at_datetime: datetime = datetime.fromtimestamp(
            raw_assignment_data.get("startTime", 0) + war_start_timestamp,
            tz=timezone.utc,
        )
        self.ends_at_datetime: datetime = datetime.now(tz=timezone.utc) + timedelta(
            seconds=raw_assignment_data["expiresIn"]
        )
        self.flags: int = raw_assignment_data["setting"]["flags"]

    @property
    def unique_task_types(self) -> set[AssignmentTaskType]:
        return {t.type for t in self.tasks}

    class Task:
        def __init__(self, task: dict, current_progress: int | float) -> None:
            self._type: int = task["type"]
            self.type: AssignmentTaskType = AssignmentTaskType(self._type)
            self.progress: int | float = current_progress
            self.values_dict: dict[int, int] = dict(
                zip(task["valueTypes"], task["values"])
            )
            self.tracker: BaseTrackerEntry | None = None

            self.faction: Faction | None = Factions.get_from_identifier(
                number=self.values_dict.get(1)
            )
            self.personal: bool = self.values_dict.get(2, 0) == 1
            self.goal: int | None = self.values_dict.get(3)
            self.target_id: int | None = self.values_dict.get(4)
            self.equipment_id: int | None = self.values_dict.get(5)
            self.equipment_type: int | None = self.values_dict.get(6)
            self.objective_type: int | None = self.values_dict.get(7)
            self.minimum_squad_size: int | None = self.values_dict.get(8)
            self.minimum_difficulty: int | None = self.values_dict.get(9)
            self.mission_type: int | None = self.values_dict.get(10)
            self.galaxy_location_type: int | None = self.values_dict.get(11)
            self.sector_index: int | None = None
            self.planet_index: int | None = None
            match self.galaxy_location_type:
                case 1:
                    self.planet_index: int | None = self.values_dict.get(12)
                case 2:
                    self.sector_index: int | None = self.values_dict.get(12)
                case 0:
                    pass
                case _:
                    if self.galaxy_location_type is not None:
                        print(f"New Galaxy Location Type: {self}")

        @property
        def progress_perc(self) -> float:
            """Returns the progress of the task as a float (0-1)"""
            return self.progress / self.goal

        @property
        def health_bar(self) -> str:
            """Returns a health_bar based on the task type and progress"""
            anim = False
            increasing = False
            if self.tracker and self.tracker.change_rate_per_hour != 0:
                anim = True
                increasing = self.tracker.change_rate_per_hour > 0

            match self.type:
                case (
                    AssignmentTaskType.Extract
                    | AssignmentTaskType.ExtractWith
                    | AssignmentTaskType.Objective
                    | AssignmentTaskType.PlayMission
                    | AssignmentTaskType.Donation
                    | AssignmentTaskType.HoldLocationsUntilEnd
                    | AssignmentTaskType.LiberateLocationsCount
                ):
                    return health_bar(
                        perc=self.progress_perc,
                        faction=Factions.humans,
                        anim=anim,
                        increasing=increasing,
                    )
                case (
                    AssignmentTaskType.Kill
                    | AssignmentTaskType.UseEquipment
                    | AssignmentTaskType.MissionComplete
                    | AssignmentTaskType.OperationComplete
                    | AssignmentTaskType.DefendFromAttacks
                ):
                    return health_bar(
                        perc=self.progress_perc,
                        faction=self.faction or "MO",
                        anim=anim,
                        increasing=increasing,
                    )
                case AssignmentTaskType.NetLiberation:
                    return health_bar(
                        perc=0.5,
                        faction=Factions.automaton,
                        empty_colour="green",
                    )
                case _:
                    return ""

    class Reward:
        def __init__(
            self, raw_reward_data: dict, endpoint_items: dict[int, EndpointItem]
        ):
            self.type: int = raw_reward_data.get("type")
            self.id: int = raw_reward_data.get("id32")
            self.amount: int = raw_reward_data.get("amount")
            self.endpoint_item: EndpointItem | None = endpoint_items.get(self.id, None)

        def __repr__(self):
            return f"Reward({self.amount}x{self.endpoint_item.name if self.endpoint_item is not None else f'Item #{self.id}'})"

        def __hash__(self):
            return hash((self.id))

        def __eq__(self, target):
            if not isinstance(target, type(self)):
                return False
            return self.id == target.id

from enum import Enum


class CampaignType(Enum):
    Liberation = 0
    """Regular liberation campaigns"""
    Recon = 1
    """Campaigns that don't do any damage to planets"""
    HighPriority = 2
    """High priority campaigns that have a marker on the map"""
    Attrition = 3
    """Sieges tied to a global resource"""
    Event = 4
    """Campaigns with an event on the planet"""


class EventType(Enum):
    UrgentLiberation = 0
    """Planet is owned by non-human faction and marked on the map

    Planet changes owner if event is won by Helldivers"""
    Defence = 1
    """Human owned planet is attacked by the enemy with a duration
    
    Planet changes owner if event is won by Helldivers"""
    Invasion = 2
    """Human owned planet attacked by non-human faction
    
    Planet does not change owner if event is won"""


class SpaceStationType(Enum):
    UNKNOWN = 0
    DSS = 749875195

    @classmethod
    def _missing_(cls, value):
        return SpaceStationType.UNKNOWN


class AssignmentTaskType(Enum):
    """The names I have given for Assignment Task Types\n
    UNKNOWN = -1\n
    Extract = 1\n
    ExtractWith = 2\n
    Kill = 3\n
    Objective = 4\n
    PlayMission = 5\n
    UseEquipment = 6\n
    MissionComplete = 7\n
    PersonalOrder = 8\n
    OperationComplete = 9\n
    Donation = 10\n
    LiberateLocationsSpecific = 11\n
    DefendFromAttacks = 12\n
    HoldLocationsUntilEnd = 13\n
    LiberateLocationsCount = 14\n
    NetLiberation = 15
    """

    UNKNOWN = -1

    Extract = 1
    ExtractWith = 2
    Kill = 3
    Objective = 4
    PlayMission = 5
    UseEquipment = 6
    MissionComplete = 7
    PersonalOrder = 8
    OperationComplete = 9
    Donation = 10
    LiberateLocationsSpecific = 11
    DefendFromAttacks = 12
    HoldLocationsUntilEnd = 13
    LiberateLocationsCount = 14
    NetLiberation = 15

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class ControlCentrePage(Enum):
    Overview = 0
    ActiveCampaign = 1
    PastCampaigns = 2


class ControlCentreStatus(Enum):
    UNKNOWN = -1
    In_Progress = 0
    Success = 2
    Failed = 3

    @classmethod
    def _missing_(cls, value):
        return cls(-1)


class ItemCategory(Enum):
    ARMOR = -7
    HELMET = -6
    CAPE = -5
    THROWABLE_WEAPON = -4
    SIDEARM_WEAPON = -3
    PRIMARY_WEAPON = -2
    UNKNOWN = -1
    UNOBTAINABLE = 0
    LOADOUT_ITEM = 1
    WEAPON_CUSTOMISATION = 2
    CUSTOMISATION_KIT = 3
    CUSTOMISATION_SET = 4
    BOOSTER = 5
    BOOSTER_PACK = 6
    VICTORY_POSE = 7
    EMOTE = 8
    PLAYER_CARD = 9
    STRATAGEM = 10
    STRATAGEM_PERMIT = 11
    STRATAGEM_UPGRADE = 12
    VOICE_PACK = 13
    PROGRESSION_PACKAGE_KEY = 14
    SAMPLE = 15
    DIFFICULTY_ITEM = 16
    BODY = 17
    CURRENCY = 18
    SHIP_MODULE_EFFECT = 19
    PROGRESSION_PACKAGE_LEVEL = 20
    ITEM_PACKAGE = 21
    COUNT = 22
    TITLE = 23

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


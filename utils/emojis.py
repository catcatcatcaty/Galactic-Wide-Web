from dataclasses import dataclass


@dataclass
class Emojis:

    @dataclass
    class ControlCentre:
        overview = "<:ss:1529603667534032897>"
        active_campaigns = "<:ss:1529604265968934912>"
        past_campaigns = "<:ss:1529604265968934913>"

    @dataclass
    class CommunityIcons:
        arsenal = "<:ss:1529604265968934914>"

    @dataclass
    class Items:
        medal = "<:ss:1529604265968934915>"
        common_sample = "<:ss:1529604265968934916>"
        rare_sample = "<:ss:1529604265968934917>"
        requisition_slip = "<:ss:1529604265968934918>"
        super_credit = "<:ss:1529604265968934919>"
        cape = "<:ss:1529604265968934920>"
        armor = "<:ss:1529604265968934921>"
        helmet = "<:ss:1529604265968934922>"
        primary_weapon = "<:ss:1529604291092811776>"
        sidearm_weapon = "<:ss:1529604291092811777>"
        throwable_weapon = "<:ss:1529604291092811778>"
        player_card = "<:ss:1537041758066585600>"

    @dataclass
    class DefenceIcons:
        automaton = "<:ss:1529604291092811779>"
        terminids = "<:ss:1529604291092811780>"
        illuminate = "<:ss:1529604291092811781>"

    @dataclass
    class RegionIcons:
        @dataclass
        class Automaton:
            _1 = "<:ss:1529604291092811783>"
            _2 = "<:ss:1529604291092811784>"
            _3 = "<:ss:1529604291092811785>"
            _4 = "<:ss:1529604291092811786>"
            special1 = "<:ss:1529604291092811787>"
            special2 = "<:ss:1529604312110477312>"
            special3 = "<:ss:1529604312110477313>"
            special4 = "<:ss:1529604312110477314>"

        @dataclass
        class Terminids:
            _1 = "<:ss:1529604312110477315>"
            _2 = "<:ss:1529604312110477316>"
            _3 = "<:ss:1529604312110477317>"
            _4 = "<:ss:1529604312110477318>"

        @dataclass
        class Illuminate:
            _1 = "<:ss:1529604312110477319>"
            _2 = "<:ss:1529604312110477320>"
            _3 = "<:ss:1529604312110477321>"
            _4 = "<:ss:1529604312110477322>"

        @dataclass
        class Humans:
            _1 = "<:ss:1529604312110477323>"
            _2 = "<:ss:1529604312110477324>"
            _3 = "<:ss:1529604312110477325>"
            _4 = "<:ss:1529604312110477326>"

    @dataclass
    class Icons:
        discord = "<:ss:1531336816353878016>"
        kofi = "<:ss:1529604333589508097>"
        github = "<:ss:1529604333589508098>"
        wiki = "<:ss:1529604333589508099>"
        hdc = "<:ss:1529604333589508100>"
        victory = "<:ss:1529604333589508101>"
        high_prio_campaign = "<:ss:1529604333589508102>"
        mo = "<:ss:1529604333589508103>"
        mo_task_complete = "<:ss:1529604333589508104>"
        mo_task_incomplete = "<:ss:1529604333589508105>"
        steam = "<:ss:1529604333589508106>"
        playstation = "<:ss:1529604333589508107>"
        xbox = "<:ss:1529612019441872896>"
        new_icon = "<:ss:1529612019441872897>"
        blank = "<:ss:1537042385760956418>"

    @dataclass
    class Factions:
        humans = "<:ss:1529612019441872898>"
        terminids = "<:ss:1529612019441872899>"
        automaton = "<:ss:1529612019441872900>"
        illuminate = "<:ss:1529612019441872901>"

    @dataclass
    class FactionColours:
        humans = "<:ss:1529612019441872902>"
        terminids = "<:ss:1529612019441872903>"
        automaton = "<:ss:1529612019441872904>"
        illuminate = "<:ss:1529612019441872905>"
        mo = "<:ss:1529612019441872906>"
        empty = "<:ss:1529612019441872907>"
        green = "<:ss:1529612019441872908>"

    @dataclass
    class FactionColoursAnim:
        mo_increasing = "<a:ss:1529612019441872909>"
        mo_decreasing = "<a:ss:1529612019441872910>"
        dss_increasing = "<a:ss:1529612041537458176>"
        dss_decreasing = "<a:ss:1529612041537458177>"
        humans_increasing = "<a:ss:1529612041537458178>"
        humans_decreasing = "<a:ss:1529612041537458179>"
        terminids_increasing = "<a:ss:1529612041537458180>"
        terminids_decreasing = "<a:ss:1529612041537458181>"
        automaton_increasing = "<a:ss:1529612041537458182>"
        automaton_decreasing = "<a:ss:1529612041537458183>"
        illuminate_increasing = "<a:ss:1529612041537458184>"
        illuminate_decreasing = "<a:ss:1529612041537458185>"

    @dataclass
    class Decoration:
        left_banner = "<:ss:1529612041537458186>"
        right_banner = "<:ss:1529612041537458187>"
        alert_icon = "<a:ss:1529612041537458188>"

    @dataclass
    class Stratagems:
        up = "<:ss:1529612041537458189>"
        down = "<:ss:1529612041537458190>"
        left = "<:ss:1529612041537458191>"
        right = "<:ss:1529612041537458192>"

    class SpaceStations:
        @dataclass
        class DSS:
            icon = "<:ss:1529612065889583104>"
            orbital_blockade = "<:ss:1529612065889583105>"
            heavy_ordnance_distribution = "<:ss:1529612065889583106>"
            eagle_storm = "<:ss:1529612065889583107>"
            operational_support = "<:ss:1529612065889583108>"
            eagle_blockade = "<:ss:1529612065889583109>"

    @dataclass
    class Weather:
        intense_heat = "<:ss:1529612065889583110>"
        fire_tornadoes = "<:ss:1529612065889583111>"
        extreme_cold = "<:ss:1529612065889583112>"
        blizzards = "<:ss:1529612065889583113>"
        tremors = "<:ss:1529612065889583114>"
        acid_storms = "<:ss:1529612065889583115>"
        ion_storms = "<:ss:1529612065889583116>"
        meteor_storms = "<:ss:1529612065889583117>"
        rain_storms = "<:ss:1529612065889583118>"
        sandstorms = "<:ss:1529612089243480064>"
        thick_fog = "<:ss:1529612089243480065>"
        volcanic_activity = "<:ss:1529612089243480066>"

    @dataclass
    class Subfactions:
        predator_strain = "<:ss:1529612202938474498>"
        jet_brigade = "<:ss:1529612202938474499>"
        incineration_corps = "<:ss:1529612202938474500>"
        the_great_host = "<:ss:1529612202938474501>"
        spore_burst_strain = "<:ss:1529612202938474502>"
        rupture_strain = "<:ss:1529612202938474503>"
        dragonroaches = "<:ss:1529612202938474504>"
        hive_lords = "<:ss:1529612202938474505>"
        cyborgs = "<:ss:1529612202938474506>"
        mindless_masses = "<:ss:1529612202938474507>"
        appropriators = "<:ss:1529612202938474508>"
        heavy_seaf_presence = "<:ss:1537390703330467840>"
        vote_snatchers = "<:ss:1537391055370977280>"

    @dataclass
    class PlanetFeatures:
        black_hole = "<:ss:1529612224694329347>"
        cfcsas = "<:ss:1529612245879754753>"
        hive_world = "<:ss:1529612224694329344>"
        centre_of_science = "<:ss:1529612245879754752>"
        xenoentomology_centre = "<:ss:1529612245879754752>"
        factory_hub = "<:ss:1529612224694329355>"
        fractured_planet = "<:ss:1529612224694329347>"
        deep_mantle_forge_complex = "<:ss:1529612224694329355>"
        helldiver_training_facilities = "<:ss:1529612224694329360>"
        max_sec_city_construction_site = "<:ss:1529612224694329355>"
        new_hope_city = "<:ss:1529612245879754753>"
        new_aspiration_city = "<:ss:1529612245879754753>"
        new_yearning_city = "<:ss:1529612245879754753>"
        ultramafic_mine = "<:ss:1529612224694329355>"
        e711_extraction_facility = "<:ss:1529612224694329355>"
        cecod = "<:ss:1529612224694329360>"
        pandora_base = "<:ss:1529612224694329360>"
        exostorm = "<:ss:1529612224694329358>"
        void = "<:ss:1529612224694329359>"
        terminid_research_preserve = "<:ss:1529612224694329360>"
        negative_energy_labratory = "<:ss:1529612245879754752>"
        tyranny_park_2 = "<:ss:1529612245879754753>"
        tcs_plus = "<:ss:1529612245879754754>"

    @dataclass
    class Flags:
        en = "🇬🇧"
        fr = "🇫🇷"
        de = "🇩🇪"
        it = "🇮🇹"
        pt_br = "🇧🇷"
        ru = "🇷🇺"
        es = "🇪🇸"
        zh_hans = "🇨🇳"
        zh_hant = "🇨🇳"
        tr = "🇹🇷"

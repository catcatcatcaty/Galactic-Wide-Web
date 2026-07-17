from disnake import Embed, Colour

from data.lists import CUSTOM_COLOURS, STRATAGEM_IMAGE_LINKS
from utils.api_wrapper.models import GlobalEvent, Planet
from utils.mixins import EmbedReprMixin


class global_events_embed(Embed, EmbedReprMixin):
    def __init__(
        self,
        container_json: dict,
        global_event: GlobalEvent,
        planets: dict[int, Planet],
        with_expiry_time: bool = False,
    ):
        super().__init__(
            accent_colour=Colour.from_rgb(*CUSTOM_COLOURS["MO"])
        )
        content = f""
        if global_event.flag == 0:
            if not global_event.planet_indices:
                specific_planets = container_json["all_planets"]
            else:
                spec_planets_list = [
                    planets.get(index) for index in global_event.planet_indices
                ]
                specific_planets = "\n-# " + "\n- ".join(
                    [p.names.get("en-GB", str(p.index)) for p in spec_planets_list if p]
                )
            for effect in global_event.effects:
                if "UNKNOWN" in effect.planet_effect["name"]:
                    content += f"\nUNKNOWN effect (ID {effect.id})\n{effect.effect_description['simplified_name']}{container_json['active_on_planets'].format(planets=specific_planets)}"
                    if effect.found_enemy:
                        content += f"\n{container_json['enemy_identified']}: {effect.found_enemy}"
                    if effect.found_stratagem:
                        content += f"\n{container_json['strat_identified']}: {effect.found_stratagem}"
                    if effect.found_booster:
                        content += f"\n{container_json['booster_identified']}: {effect.found_booster['name']}"
                else:
                    content += f"\n{effect.planet_effect['name']}"
                    if effect.planet_effect["description_long"]:
                        content += (
                            f"\n-# {effect.planet_effect['description_long']}"
                        )
                    if effect.planet_effect["description_short"]:
                        if effect.effect_type == 32:
                            if effect.found_stratagem:
                                effect.planet_effect["description_short"] = (
                                    effect.planet_effect["description_short"].replace(
                                        "#V_ONE", effect.found_stratagem
                                    )
                                )
                        content += (
                            f"\n-# {effect.planet_effect['description_short']}"
                        )
                    content += f"{container_json['active_on_planets'].format(planets=specific_planets)}"
        else:
            for chunk in global_event.split_message:
                content += f"\n{chunk}"
        if with_expiry_time:
            content += (
                f"-# {container_json['expires']} <t:{global_event.expire_time}:R>"
            )
        content += (
            f"\n-# {container_json['global_event']} #{global_event.id}"
        )

        self.add_field(f"# {global_event.title if global_event.title else container_json['new_event']}", content)


class global_events_command_embed(Embed, EmbedReprMixin):
    def __init__(self, global_event: GlobalEvent, planets: list[Planet]) -> None:
        super().__init__(
            accent_colour=Colour.blurple()
        )
        content = f""
        for effect in global_event.effects:
            #image subsectioning not possible in embeds
            #section = ui.Section(
                #ui.TextDisplay(""),
                #accessory=ui.Thumbnail(
                #    "https://cdn.discordapp.com/attachments/1212735927223590974/1422512588973015081/0xa92d559bf3ae174.png?ex=692eae96&is=692d5d16&hm=1a6a92832ea0b6746ec96b5cc6c6c7894be3d5bc828a8d23a89e16782947c481&"
                #),
            #)
            text: str = effect.effect_description["format_desc"]

            if (
                effect.percent
                and effect.percent > 0
                or effect.count
                and effect.count > 0
            ):
                text = text.replace("{changed}", "increased")
            elif (
                effect.percent
                and effect.percent < 0
                or effect.count
                and effect.count < 0
            ):
                text = text.replace("{changed}", "decreased")
            if effect.percent:
                text = text.replace("{amount}", f"{effect.percent}%")
            elif effect.count:
                text = text.replace("{amount}", f"{effect.count}")
            elif effect.effect_type in [56]:
                text = text.replace("{amount}", f"an undisclosed amount")

            if "cooldown" in text.lower():
                text += " seconds"

            if effect.found_enemy:
                text = text.replace("{enemy}", effect.found_enemy.upper())

            if effect.found_stratagem:
                text = text.replace("{stratagem}", effect.found_stratagem.upper())

            #image subsectioning not possible in embeds
            #for stratagem in STRATAGEM_IMAGE_LINKS.keys():
                #if stratagem.lower() in text.lower():
                     #section.accessory = ui.Thumbnail(STRATAGEM_IMAGE_LINKS[stratagem])

            if not global_event.planet_indices:
                text += "\n- active on **ALL PLANETS**"
            else:
                active_on_planets = [
                    planets.get(i) for i in global_event.planet_indices
                ]
                text += "\n- active on:\n  - " + "\n  - ".join(
                    [
                        f"**{p.names.get('en-GB', str(p.index))}**"
                        for p in active_on_planets
                        if p
                    ]
                )

            content += text
            if len(global_event.effects) > 1:
                content += f"\n"

        content += f"\n Expires <t:{global_event.expire_time}:R>"

        if global_event.title:
            self.add_field(f"# {global_event.title}", content)
        else:
            self.add_field(".", content)

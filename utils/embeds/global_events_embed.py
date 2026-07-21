from disnake import Embed, Colour

from data.lists import CUSTOM_COLOURS, STRATAGEM_IMAGE_LINKS
from utils.api_wrapper.models import GlobalEvent, Planet
from utils.mixins import EmbedReprMixin


class global_events_embed(Embed, EmbedReprMixin):
    def __init__(
        self,
        lang_code: str,
        container_json: dict,
        global_event: GlobalEvent,
        planets: dict[int, Planet],
        with_expiry_time: bool = False,
        image_url: str = None,
        attachment_url: str = None,
    ):
        super().__init__(
            accent_colour=Colour.from_rgb(*CUSTOM_COLOURS["MO"])
        )
        content = f""
        ### FLUXER ATTACHMENTS BROKEN
        #if image_url:
            #self.set_image(image_url)
        #elif attachment_url:
            #self.set_image(attachment_url)
        if global_event.flag == 0:
            if not global_event.planet_indices:
                specific_planets = container_json["all_planets"]
            else:
                spec_planets_list = [
                    planets.get(index) for index in global_event.planet_indices
                ]
                specific_planets = "\n-# " + "\n- ".join(
                    [p.names.get(lang_code, p.name) for p in spec_planets_list if p]
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
from disnake import Embed, Colour

from data.lists import CUSTOM_COLOURS
from utils.api_wrapper.models import GlobalEvent, Planet
from utils.containers import GWEContainer
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
            colour=Colour.from_rgb(*CUSTOM_COLOURS["MO"])
        )
        content = f""
        if image_url:
            self.set_image(image_url)
        elif attachment_url:
            self.set_image(attachment_url)
        title = f"{global_event.title if global_event.title else container_json['new_event']}"
        if global_event.assignment_id:
            title += f"\nRelated to Assignment #{global_event.assignment_id}"
        if global_event.effects != []:
            if not global_event.planet_indices:
                specific_planets = container_json["all_planets"]
            else:
                spec_planets_list = [
                    planets.get(index) for index in global_event.planet_indices
                ]
                specific_planets = "\n-# " + "\n- ".join(
                    [p.names.get(lang_code, p.name) for p in spec_planets_list if p]
                )
            effects_text = ""
            for effect in global_event.effects:
                effect_container = GWEContainer(effect, [], False, False)
                gwe_content = (
                    "\n"
                    + effect_container.components[0].content
                    + effect_container.components[1].content
                    + "\n"
                )
                effects_text += gwe_content
                effects_text += f"\n ### {container_json['active_on_planets']}:{specific_planets}"
                content += effects_text or "No effects present"
        else:
            for chunk in global_event.split_message:
                content += f"\n{chunk}"
        if with_expiry_time:
            content += (
                f"\n-# {container_json['expires']} <t:{global_event.expire_time}:R>"
            )
        content += (
            f"\n-# {container_json['global_event']} #{global_event.id}"
        )

        self.add_field(title, content)
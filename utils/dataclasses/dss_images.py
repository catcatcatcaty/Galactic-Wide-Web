from dataclasses import dataclass


@dataclass
class DSSImages:
    class EAGLE_STORM:
        active = "https://fluxerusercontent.com/attachments/1476525402340249794/1531583373829484544/1000108676.png"
        preparing = "https://fluxerusercontent.com/attachments/1476525402340249794/1531583373829484545/1000108677.png"
        on_cooldown = "https://fluxerusercontent.com/attachments/1476525402340249794/1531583373829484546/1000108678.png"

    class ORBITAL_BLOCKADE:
        active = "https://fluxerusercontent.com/attachments/1476525402340249794/1531583394163470336/1000108679.png"
        preparing = "https://fluxerusercontent.com/attachments/1476525402340249794/1531583394163470337/1000108680.png"
        on_cooldown = "https://fluxerusercontent.com/attachments/1476525402340249794/1531583394163470338/1000108681.png"

    class HEAVY_ORDNANCE_DISTRIBUTION:
        active = "https://fluxerusercontent.com/attachments/1476525402340249794/1531583416036765696/1000108682.png"
        preparing = "https://fluxerusercontent.com/attachments/1476525402340249794/1531583416036765697/1000108683.png"
        on_cooldown = "https://fluxerusercontent.com/attachments/1476525402340249794/1531583416036765698/1000108684.png"

    UNKNOWN = "https://fluxerusercontent.com/attachments/1476525402340249794/1531583433547980800/1000108685.png"

    def get(ta_name: str, status: str) -> str | None:
        ta_name = ta_name.replace(" ", "_").upper()
        try:
            ta_obj = getattr(DSSImages, ta_name, None)
            if ta_obj is None:
                return DSSImages.UNKNOWN
            return getattr(ta_obj, status)
        except AttributeError:
            return DSSImages.UNKNOWN

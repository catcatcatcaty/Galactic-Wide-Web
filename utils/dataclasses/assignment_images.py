from dataclasses import dataclass
from utils.dataclasses.enums import AssignmentTaskType


@dataclass
class AssignmentImages:
    _2 = "https://fluxerusercontent.com/attachments/1476525402340249794/1530882684606222336/1000108521.png"
    _3 = "https://fluxerusercontent.com/attachments/1476525402340249794/1530883185666170880/1000108522.png"
    _7 = "https://fluxerusercontent.com/attachments/1476525402340249794/1530882684606222336/1000108521.png"
    _8 = "https://fluxerusercontent.com/attachments/1476525402340249794/1530883756234117120/1000108523.png"
    _9 = "https://fluxerusercontent.com/attachments/1476525402340249794/1530882684606222336/1000108521.png"
    _11 = "https://fluxerusercontent.com/attachments/1476525402340249794/1530882334553804800/1000108520.png"
    _12 = "https://fluxerusercontent.com/attachments/1476525402340249794/1530883989068328960/1000108524.png"
    _13 = "https://fluxerusercontent.com/attachments/1476525402340249794/1530883989068328960/1000108524.png"
    _15 = "https://fluxerusercontent.com/attachments/1476525402340249794/1530882684606222336/1000108521.png"

    def get(task_type: AssignmentTaskType) -> str:
        """Gets the appropriate Assignment Icon"""
        return getattr(
            AssignmentImages,
            f"_{task_type.value}",
            "https://fluxerusercontent.com/attachments/1476525402340249794/1530882334553804800/1000108520.png",
        )

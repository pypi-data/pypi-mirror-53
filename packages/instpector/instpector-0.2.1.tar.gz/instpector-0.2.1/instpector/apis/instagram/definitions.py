from collections import namedtuple

TUser = namedtuple("TUser", "id username full_name is_private")

TPageInfo = namedtuple("TPageInfo", "end_cursor has_next_page")

TProfile = namedtuple("TProfile", (
    "id username biography is_private followers_count following_count"
))

TTimelinePost = namedtuple("TTimelinePost", "id timestamp is_video like_count comment_count")

TStoryReelItem = namedtuple("TStoryReelItem", (
    "id timestamp expire_at audience is_video view_count display_resources video_resources"
))

TStoryViewer = namedtuple("TStoryViewer", "id username")

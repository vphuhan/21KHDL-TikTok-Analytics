from __future__ import annotations
from ..exceptions import InvalidResponseException
from .video import Video

from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from ..tiktok import TikTokApi


class Trending:
    """Contains static methods related to trending objects on TikTok."""

    parent: TikTokApi

    @staticmethod
    # async def videos(count=30, cursor=0, **kwargs) -> Iterator[Video]:
    #     """
    #     Returns Videos that are trending on TikTok.

    #     Args:
    #         count (int): The amount of videos you want returned.

    #     Returns:
    #         async iterator/generator: Yields TikTokApi.video objects.

    #     Raises:
    #         InvalidResponseException: If TikTok returns an invalid response, or one we don't understand.

    #     Example Usage:
    #         .. code-block:: python

    #             async for video in api.trending.videos():
    #                 # do something
    #     """
    #     found = 0
    #     while found < count:
    #         params = {
    #             "from_page": "fyp",
    #             # "from_page": "explore",
    #             "count": 35,
    #             "cursor": cursor,
    #         }

    #         resp = await Trending.parent.make_request(
    #             url="https://www.tiktok.com/api/recommend/item_list/",
    #             params=params,
    #             headers=kwargs.get("headers"),
    #             session_index=kwargs.get("session_index"),
    #         )

    #         if resp is None:
    #             raise InvalidResponseException(
    #                 resp, "TikTok returned an invalid response."
    #             )
    #         print(f"found: {found} -- resp.get('itemList', []): {len(resp.get('itemList', []))}")
    #         for video in resp.get("itemList", []): # lấy tối đa 3
    #             if found < count:
    #                 yield Trending.parent.video(data=video)
    #                 found += 1

    #         if not resp.get("hasMore", False):
    #             return
    
    # async def videos(count=30, cursor=0, **kwargs) -> Iterator[Video]:
    async def videos(cursor=0, **kwargs) -> Iterator[Video]:
        """
        Returns Videos that are trending on TikTok.

        Args:
            count (int): The amount of videos you want returned.

        Returns:
            async iterator/generator: Yields TikTokApi.video objects.

        Raises:
            InvalidResponseException: If TikTok returns an invalid response, or one we don't understand.

        Example Usage:
            .. code-block:: python

                async for video in api.trending.videos():
                    # do something
        """
        # found = 0

        params = {
            "from_page": "fyp",
            # "from_page": "explore",
            "count": 35,
            "cursor": cursor,
            "language": "vi"
        }

        resp = await Trending.parent.make_request(
            url="https://www.tiktok.com/api/recommend/item_list/",
            params=params,
            headers=kwargs.get("headers"),
            session_index=kwargs.get("session_index"),
        )

        if resp is None:
            raise InvalidResponseException(
                resp, "TikTok returned an invalid response."
            )
        # print(f"resp.get('itemList', []): {len(resp.get('itemList', []))}")
        for video in resp.get("itemList", []): # lấy tối đa 35
            # if found < count:
            yield Trending.parent.video(data=video)
            # found += 1

        if not resp.get("hasMore", False):
            return

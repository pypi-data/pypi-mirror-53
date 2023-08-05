from dayangpy.api.base import BaseAPI
import dayangpy.constant as const
import datetime


class DaYangRank(BaseAPI):
    """
    媒体榜单相关接口
    """

    API_BASE_URL = "http://gateway.bigdata.cloud.dayang.com.cn:8088"

    def get_hotsearch(self, site_id, classify, **kwargs):
        """
        热搜榜单
        """
        size = kwargs.get("size", 10)
        classify = const.HOT_SEARCH_DICT.get(site_id, None).get(classify, None)

        result = self._get(
            f"/openapi4hoge/v1/hotSearch/{site_id}/{classify}",
            params={"size": int(size)},
        )
        return result.get("result", None).get("items")

    def get_wechat(self, sort_name, **kwargs):
        """
        微信榜单
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        billboard_time_type = kwargs.get("billboard_time_type", "")
        classify_id = kwargs.get("classify_id", "")
        name_like = kwargs.get("name_like", "")
        location = kwargs.get("location", "")
        billboard_time = kwargs.get("billboard_time", now)
        scroll_id = kwargs.get("scroll_id", "")
        size = kwargs.get("size", 10)
        sort_type = kwargs.get("sort_type", "desc")
        data = {
            "billboardTimeType": billboard_time_type,
            "classifyId": classify_id,
            "nameLike": name_like,
            "location": location,
            "scrollId": scroll_id,
            "billboardTime": billboard_time,
            "size": int(size),
            "sorts": [{"sortName": sort_name, "sortType": sort_type}],
        }
        return self._post(f"/openapi4hoge/v1/wechatRank/list", json=data)

    def get_weibo(self, sort_name, **kwargs):
        """
        微博榜单
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        billboard_time_type = kwargs.get("billboard_time_type", "")
        name_like = kwargs.get("name_like", "")
        location = kwargs.get("location", "")
        billboard_time = kwargs.get("billboard_time", now)
        scroll_id = kwargs.get("scroll_id", "")
        size = kwargs.get("size", 10)
        sort_type = kwargs.get("sort_type", "desc")

        data = {
            "billboardTimeType": billboard_time_type,
            "billboardTime": billboard_time,
            "nameLike": name_like,
            "scrollId": scroll_id,
            "location": location,
            "size": int(size),
            "sorts": [{"sortName": sort_name, "sortType": sort_type}],
        }
        return self._post(f"/openapi4hoge/v1/weiboRank/list", json=data)

    def get_toutiao(self, sort_name, **kwargs):
        """
        头条榜单
        """
        billboard_time_type = kwargs.get("billboard_time_type", "")
        billboard_type = kwargs.get("billboard_type", 0)
        latest_days = kwargs.get("latest_days", 1)
        name_like = kwargs.get("name_like", "")
        scroll_id = kwargs.get("scroll_id", "")
        size = kwargs.get("size", 10)
        sort_type = kwargs.get("sort_type", "desc")

        timeEnd = datetime.datetime.now()
        timeStart = timeEnd - datetime.timedelta(days=int(latest_days))
        data = {
            "billboardTimeType": billboard_time_type,
            "nameLike": name_like,
            "billboardTimeStart": timeStart.strftime("%Y-%m-%d"),
            "billboardTimeEnd": timeEnd.strftime("%Y-%m-%d"),
            "toutiaoBillboardType": int(billboard_type),
            "size": int(size),
            "sorts": [{"sortName": sort_name, "sortType": sort_type}],
        }
        return self._post(f"/openapi4hoge/v1/weiboRank/list", json=data)

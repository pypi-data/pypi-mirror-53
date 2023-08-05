import datetime
from dayangpy.api.base import BaseAPI
import dayangpy.constant as const
from dayangpy.utils import handle_args


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

    def get_wechat(self, sort_name, sort_type, **kwargs):
        """
        微信榜单
        """

        data = handle_args(kwargs)
        data.update(sorts=[{"sortName": sort_name, "sortType": sort_type}])

        result = self._post(f"/openapi4hoge/v1/wechatRank/list", json=data)
        return result.get("result", None).get("resources", None)

    def get_weibo(self, sort_name, sort_type, **kwargs):
        """
        微博榜单
        """

        data = handle_args(kwargs)
        data.update(sorts=[{"sortName": sort_name, "sortType": sort_type}])

        result = self._post(f"/openapi4hoge/v1/weiboRank/list", json=data)
        return result.get("result", None).get("resources", None)

    def get_toutiao(self, sort_name, sort_type, latest_days, **kwargs):
        """
        头条榜单
        """
        data = handle_args(kwargs)
        time_end = datetime.datetime.now()
        time_start = time_end - datetime.timedelta(days=int(latest_days))
        data.update(billboardTimeStart=time_start.strftime("%Y-%m-%d"))
        data.update(billboardTimeEnd=time_end.strftime("%Y-%m-%d"))
        data.update(sorts=[{"sortName": sort_name, "sortType": sort_type}])

        result = self._post(f"/openapi4hoge/v1/toutiaoRank/list", json=data)
        return result.get("result", None).get("resources", None)

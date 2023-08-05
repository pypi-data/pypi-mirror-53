from dayangpy.api.base import BaseAPI
import dayangpy.constant as const
import datetime


class DaYangRank(BaseAPI):
    """
    媒体榜单相关接口
    """

    API_BASE_URL = "http://gateway.bigdata.cloud.dayang.com.cn:8088"

    def get_hotsearch(self, siteId, classify, size=10):
        """
        热搜榜单
        """
        classify = const.HOT_SEARCH_DICT.get(siteId, None).get(classify, None)

        result = self._get(
            f"/openapi4hoge/v1/hotSearch/{siteId}/{classify}",
            params={"size": int(size)},
        )
        return result.get("result", None).get("items")

    def get_wechat(
        self,
        billboardTimeType="",
        classifyId="",
        nameLike="",
        location="",
        scrollId="",
        size=10,
        sortName="poi",
        sortType="desc",
    ):
        """
        微信榜单
        """
        data = {
            "billboardTimeType": billboardTimeType,
            "classifyId": classifyId,
            "nameLike": nameLike,
            "location": location,
            "scrollId": scrollId,
            "size": int(size),
            "sorts": [{"sortName": sortName, "sortType": sortType}],
        }
        return self._post(f"/openapi4hoge/v1/wechatRank/list", json=data)

    def get_weibo(
        self,
        billboardTimeType=None,
        nameLike=None,
        location=None,
        size=10,
        sortName="poi",
        sortType="desc",
    ):
        """
        微博榜单
        """
        data = {
            "billboardTimeType": billboardTimeType,
            "nameLike": nameLike,
            "location": location,
            "size": int(size),
            "sorts": [{"sortName": sortName, "sortType": sortType}],
        }
        return self._post(f"/openapi4hoge/v1/weiboRank/list", json=data)

    def get_toutiao(
        self,
        billboardTimeType=None,
        billboardType=0,
        latest_days=1,
        nameLike=None,
        location=None,
        size=10,
        sortName="poi",
        sortType="desc",
    ):
        """
        头条榜单
        """
        timeEnd = datetime.datetime.now()
        timeStart = timeEnd - datetime.timedelta(days=int(latest_days))
        data = {
            "billboardTimeType": billboardTimeType,
            "nameLike": nameLike,
            "location": location,
            "billboardTimeStart": timeStart.strftime("%Y-%m-%d"),
            "billboardTimeEnd": timeEnd.strftime("%Y-%m-%d"),
            "toutiaoBillboardType": int(billboardType),
            "size": int(size),
            "sorts": [{"sortName": sortName, "sortType": sortType}],
        }
        return self._post(f"/openapi4hoge/v1/weiboRank/list", json=data)

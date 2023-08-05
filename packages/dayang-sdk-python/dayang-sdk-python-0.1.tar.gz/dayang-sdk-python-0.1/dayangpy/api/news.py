from dayangpy.api.base import BaseAPI
import datetime


class DaYangNews(BaseAPI):
    """
    线索搜索接口
    """

    API_BASE_URL = "http://gateway.bigdata.cloud.dayang.com.cn:8088"

    def search(
        self,
        accountIds,
        locationNames,
        mediaTypes,
        contentClassifys,
        titleLike="",
        latestTimestamp="",
        latest_days=1,
        page=1,
        pageSize=10,
    ):
        """
        线索搜索
        """
        timeEnd = datetime.datetime.now()
        timeStart = timeEnd - datetime.timedelta(days=int(latest_days))
        data = {
            "accountIds": accountIds,
            "locationNames": locationNames,
            "mediaTypes": mediaTypes,
            "contentClassifys": contentClassifys,
            "publishTimeStart": timeStart.strftime("%Y-%m-%d %H:%M:%S"),
            "publishTimeEnd": timeEnd.strftime("%Y-%m-%d %H:%M:%S"),
            "titleLike": titleLike,
            "latestTimestamp": latestTimestamp,
            "page": int(page),
            "pageSize": int(pageSize),
        }

        result = self._post(f"/openapi4hoge/v1/news/search", json=data)
        return result.get("result", None).get("datas", None)

    def detail(self, resourceId):
        """
        新闻详情信息获取
        """
        result = self._get(f"/openapi4hoge/v1/news/detail/{resourceId}")
        return result.get("result", None)

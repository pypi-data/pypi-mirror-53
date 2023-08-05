from dayangpy.api.base import BaseAPI
import datetime


class DaYangHotspot(BaseAPI):
    """
    热点事件查询相关接口
    """

    API_BASE_URL = "http://gateway.bigdata.cloud.dayang.com.cn:8088"

    def list(
        self,
        category_id=None,
        latest_days=1,
        scrollId=None,
        location=None,
        size=10,
        sortName="posttime",
        sortType="desc",
    ):
        """
        获取热点列表根据时间或者热度排序，查询条件支持地域、分类、时间
        """

        timeEnd = datetime.datetime.now()
        timeStart = timeEnd - datetime.timedelta(days=int(latest_days))
        data = {
            "classifyId": category_id,
            "scrollId": scrollId,
            "timeStart": timeStart.strftime("%Y-%m-%d %H:%M:%S"),
            "timeEnd": timeEnd.strftime("%Y-%m-%d %H:%M:%S"),
            "location": location,
            "size": int(size),
            "sorts": [{"sortName": sortName, "sortType": sortType}],
        }
        return self._post("/openapi4hoge/v1/events/list", json=data)

    def get_classify(self):
        """
        获取热点类型
        """
        return self._get(f"/openapi4hoge/v1/events/classify/list")

    def get_area_heat(self, areaId=0, latest_days=1):
        """
        地域热点地图统计
        """
        timeEnd = datetime.datetime.now()
        timeStart = timeEnd - datetime.timedelta(days=int(latest_days))
        return self._get(
            f"/openapi4hoge/v1/events/areaHeat/{int(areaId)}",
            params={
                "timeStart": timeStart.strftime("%Y-%m-%d %H:%M:%S"),
                "timeEnd": timeEnd.strftime("%Y-%m-%d %H:%M:%S"),
            },
        )

    def get_hotwords(self, contentClassifyId, topNum, latest_days=1, location=""):
        """
        热词排行列表
        """
        timeEnd = datetime.datetime.now()
        timeStart = timeEnd - datetime.timedelta(days=int(latest_days))
        return self._get(
            f"/openapi4hoge/v1/hotword/list",
            params={
                "contentClassifyId": contentClassifyId,
                "topNum": topNum,
                "timeStart": timeStart.strftime("%Y-%m-%d %H:%M:%S"),
                "timeEnd": timeEnd.strftime("%Y-%m-%d %H:%M:%S"),
                "location": location,
            },
        )

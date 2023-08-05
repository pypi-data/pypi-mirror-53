from dayangpy.api.base import BaseAPI
import datetime


class DaYangHotspot(BaseAPI):
    """
    热点事件查询相关接口
    """

    API_BASE_URL = "http://gateway.bigdata.cloud.dayang.com.cn:8088"

    def list(self, sort_name, **kwargs):
        """
        获取热点列表根据时间或者热度排序，查询条件支持地域、分类、时间
        """

        category_id = kwargs.get("category_id", "")
        scroll_id = kwargs.get("scroll_id", "")
        latest_days = kwargs.get("latest_days", 1)
        location = kwargs.get("location", "")
        full_text = kwargs.get("full_text", "")
        size = kwargs.get("size", 10)
        sort_type = kwargs.get("sort_type", "desc")

        timeEnd = datetime.datetime.now()
        timeStart = timeEnd - datetime.timedelta(days=int(latest_days))
        data = {
            "classifyId": category_id,
            "scrollId": scroll_id,
            "timeStart": timeStart.strftime("%Y-%m-%d %H:%M:%S"),
            "timeEnd": timeEnd.strftime("%Y-%m-%d %H:%M:%S"),
            "location": location,
            "fullText": full_text,
            "size": int(size),
            "sorts": [{"sortName": sort_name, "sortType": sort_type}],
        }
        return self._post("/openapi4hoge/v1/events/list", json=data)

    def get_classify(self):
        """
        获取热点类型
        """
        return self._get(f"/openapi4hoge/v1/events/classify/list")

    def get_area_heat(self, **kwargs):
        """
        地域热点地图统计
        """
        area_id = kwargs.get("area_id", 0)
        latest_days = kwargs.get("latest_days", 1)
        timeEnd = datetime.datetime.now()
        timeStart = timeEnd - datetime.timedelta(days=int(latest_days))
        return self._get(
            f"/openapi4hoge/v1/events/areaHeat/{int(area_id)}",
            params={
                "timeStart": timeStart.strftime("%Y-%m-%d %H:%M:%S"),
                "timeEnd": timeEnd.strftime("%Y-%m-%d %H:%M:%S"),
            },
        )

    def get_hotwords(self, **kwargs):
        """
        热词排行列表
        """
        content_classify_id = kwargs.get("content_classify_id", "")
        top_num = kwargs.get("top_num", "")
        latest_days = kwargs.get("latest_days", 1)
        location = kwargs.get("location", "")
        timeEnd = datetime.datetime.now()
        timeStart = timeEnd - datetime.timedelta(days=int(latest_days))
        return self._get(
            f"/openapi4hoge/v1/hotword/list",
            params={
                "contentClassifyId": content_classify_id,
                "topNum": top_num,
                "timeStart": timeStart.strftime("%Y-%m-%d %H:%M:%S"),
                "timeEnd": timeEnd.strftime("%Y-%m-%d %H:%M:%S"),
                "location": location,
            },
        )

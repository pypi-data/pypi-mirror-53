import datetime
from dayangpy.api.base import BaseAPI
from dayangpy.utils import handle_args


class DaYangHotspot(BaseAPI):
    """
    热点事件查询相关接口
    """

    API_BASE_URL = "http://gateway.bigdata.cloud.dayang.com.cn:8088"

    def list(self, sort_name, sort_type, latest_days, **kwargs):
        """
        获取热点列表根据时间或者热度排序，查询条件支持地域、分类、时间
        """

        data = handle_args(kwargs)
        data.update(sorts=[{"sortName": sort_name, "sortType": sort_type}])
        time_end = datetime.datetime.now()
        time_start = time_end - datetime.timedelta(days=int(latest_days))
        data.update(timeStart=time_start.strftime("%Y-%m-%d %H:%M:%S"))
        data.update(timeEnd=time_end.strftime("%Y-%m-%d %H:%M:%S"))

        result = self._post("/openapi4hoge/v1/events/list", json=data)
        return result.get("result", None).get("resources", None)

    def get_classify(self):
        """
        获取热点类型
        """
        result = self._get(f"/openapi4hoge/v1/events/classify/list")
        return result.get("resultList", None)

    def get_area_heat(self, latest_days, **kwargs):
        """
        地域热点地图统计
        """
        data = handle_args(kwargs)
        time_end = datetime.datetime.now()
        time_start = time_end - datetime.timedelta(days=int(latest_days))
        data.update(timeStart=time_start.strftime("%Y-%m-%d %H:%M:%S"))
        data.update(timeEnd=time_end.strftime("%Y-%m-%d %H:%M:%S"))
        result = self._get(f"/openapi4hoge/v1/events/areaHeat", params=data)
        return result.get("result", None).get("subAreas", None)

    def get_hotwords(self, latest_days, **kwargs):
        """
        热词排行列表
        """
        data = handle_args(kwargs)
        time_end = datetime.datetime.now()
        time_start = time_end - datetime.timedelta(days=int(latest_days))
        data.update(timeStart=time_start.strftime("%Y-%m-%d %H:%M:%S"))
        data.update(timeEnd=time_end.strftime("%Y-%m-%d %H:%M:%S"))

        result = self._get(f"/openapi4hoge/v1/hotword/list", params=data)
        return result.get("result", None).get("list", None)

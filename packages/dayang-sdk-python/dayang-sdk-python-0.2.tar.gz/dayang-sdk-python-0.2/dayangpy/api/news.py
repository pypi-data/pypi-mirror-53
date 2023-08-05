import time
import datetime
from dayangpy.api.base import BaseAPI


class DaYangNews(BaseAPI):
    """
    线索搜索接口
    """

    API_BASE_URL = "http://gateway.bigdata.cloud.dayang.com.cn:8088"

    def search(self, **kwargs):
        """
        线索搜索
        """
        account_ids = kwargs.get("account_ids", [])
        location_names = kwargs.get("location_names", [])
        media_types = kwargs.get("media_types", [])
        content_classifys = kwargs.get("content_classifys", [])
        title_like = (kwargs.get("title_like", ""),)
        latest_timestamp = (kwargs.get("latest_timestamp", int(time.time())),)
        latest_days = (kwargs.get("latest_days", 1),)
        page = (kwargs.get("page", 1),)
        page_size = (kwargs.get("page_size", 10),)
        time_end = datetime.datetime.now()
        time_start = time_end - datetime.timedelta(days=int(latest_days))
        data = {
            "accountIds": account_ids,
            "locationNames": location_names,
            "mediaTypes": media_types,
            "contentClassifys": content_classifys,
            "publishTimeStart": time_start.strftime("%Y-%m-%d %H:%M:%S"),
            "publishTimeEnd": time_end.strftime("%Y-%m-%d %H:%M:%S"),
            "titleLike": title_like,
            "latestTimestamp": latest_timestamp,
            "page": int(page),
            "pageSize": int(page_size),
        }

        result = self._post(f"/openapi4hoge/v1/news/search", json=data)
        return result.get("result", None).get("datas", None)

    def detail(self, resourceId):
        """
        新闻详情信息获取
        """
        result = self._get(f"/openapi4hoge/v1/news/detail/{resourceId}")
        return result.get("result", None)

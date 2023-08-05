import time
import datetime
from dayangpy.api.base import BaseAPI
from dayangpy.utils import handle_args


class DaYangNews(BaseAPI):
    """
    线索搜索接口
    """

    API_BASE_URL = "http://gateway.bigdata.cloud.dayang.com.cn:8088"

    def search(self, latest_days, **kwargs):
        """
        线索搜索
        """
        data = handle_args(kwargs)
        time_end = datetime.datetime.now()
        time_start = time_end - datetime.timedelta(days=int(latest_days))
        data.update(publishTimeStart=time_start.strftime("%Y-%m-%d %H:%M:%S"))
        data.update(publishTimeEnd=time_end.strftime("%Y-%m-%d %H:%M:%S"))
        result = self._post(f"/openapi4hoge/v1/news/search", json=data)
        return result.get("result", None).get("datas", None)

    def get_detail(self, resource_id):
        """
        新闻详情信息获取
        """
        result = self._get(f"/openapi4hoge/v1/news/detail/{resource_id}")
        return result.get("result", None)

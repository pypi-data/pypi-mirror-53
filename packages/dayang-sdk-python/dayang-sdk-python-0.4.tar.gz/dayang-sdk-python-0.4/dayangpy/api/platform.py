from dayangpy.api.base import BaseAPI
from dayangpy.utils import handle_args


class DaYangPlatform(BaseAPI):
    """
    账号列表查询接口
    """

    API_BASE_URL = "http://gateway.bigdata.cloud.dayang.com.cn:8088"

    def get_website(self, **kwargs):
        """
        账号列表查询-网站
        """
        data = handle_args(kwargs)

        result = self._get(f"/openapi4hoge/v1/account/list/website", params=data)
        return result.get("result", None).get("datas")

    def get_wechat(self, **kwargs):
        """
        账号列表查询-微信
        """
        data = handle_args(kwargs)
        result = self._get(f"/openapi4hoge/v1/account/list/wechat", params=data)
        return result.get("result", None).get('datas', None)

    def get_weibo(self, **kwargs):
        """
        账号列表查询-微博
        """
        data = handle_args(kwargs)
        result = self._get(f"/openapi4hoge/v1/account/list/weibo", params=data)
        return result.get('result', None).get('datas', None)

    def get_area(self, area_id):
        """
        区域列表查询
        """
        result = self._get(f"/openapi4hoge/v1/area/list/{area_id}")
        return result.get("resultList", None)

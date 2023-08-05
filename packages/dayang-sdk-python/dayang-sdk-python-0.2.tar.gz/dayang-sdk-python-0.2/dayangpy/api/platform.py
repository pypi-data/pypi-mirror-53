from dayangpy.api.base import BaseAPI


class DaYangPlatform(BaseAPI):
    """
    账号列表查询接口
    """

    API_BASE_URL = "http://gateway.bigdata.cloud.dayang.com.cn:8088"

    def get_website(self, **kwargs):
        """
        账号列表查询-网站
        """
        name = kwargs.get("name", "")
        page = kwargs.get("page", 1)
        page_size = kwargs.get("page_size", 10)
        data = self._get(
            f"/openapi4hoge/v1/account/list/website",
            params={"page": int(page), "pageSize": int(page_size), "like": name},
        )
        return data.get("result", None).get("datas")

    def get_wechat(self, **kwargs):
        """
        账号列表查询-微信
        """
        name = kwargs.get("name", "")
        page = kwargs.get("page", 1)
        page_size = kwargs.get("page_size", 10)
        data = self._get(
            f"/openapi4hoge/v1/account/list/wechat",
            params={"page": int(page), "page_size": int(page_size), "like": name},
        )
        return data.get("result", None)

    def get_weibo(self, **kwargs):
        """
        账号列表查询-微信
        """
        name = kwargs.get("name", "")
        page = kwargs.get("page", 1)
        page_size = kwargs.get("page_size", 10)
        data = self._get(
            f"/openapi4hoge/v1/account/list/weibo",
            params={"page": int(page), "pageSize": int(page_size), "like": name},
        )
        return data.get("reuslt", None).get("datas", None)

    def get_area(self, area_id):
        """
        区域列表查询
        """
        data = self._get(f"/openapi4hoge/v1/area/list/{area_id}")
        return data.get("resultList", None)

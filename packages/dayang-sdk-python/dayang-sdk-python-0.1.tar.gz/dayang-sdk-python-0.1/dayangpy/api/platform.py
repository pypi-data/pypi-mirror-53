from dayangpy.api.base import BaseAPI


class DaYangPlatform(BaseAPI):
    """
    账号列表查询接口
    """

    API_BASE_URL = "http://gateway.bigdata.cloud.dayang.com.cn:8088"

    def get_website(self, name, page=1, pageSize=10):
        """
        账号列表查询-网站
        """
        data = self._get(
            f"/openapi4hoge/v1/account/list/website",
            params={"page": int(page), "pageSize": int(pageSize), "like": name},
        )
        return data.get("result", None).get("datas")

    def get_wechat(self, name, page=1, pageSize=10):
        """
        账号列表查询-微信
        """

        data = self._get(
            f"/openapi4hoge/v1/account/list/wechat",
            params={"page": int(page), "pageSize": int(pageSize), "like": name},
        )
        return data.get("result", None)

    def get_weibo(self, name, page=1, pageSize=10):
        """
        账号列表查询-微信
        """
        data = self._get(
            f"/openapi4hoge/v1/account/list/weibo",
            params={"page": int(page), "pageSize": int(pageSize), "like": name},
        )
        return data.get("reuslt", None).get("datas", None)

    def get_area(self, parentAreaId):
        """
        区域列表查询
        """
        data = self._get(f"/openapi4hoge/v1/area/list/{parentAreaId}")
        return data.get("resultList", None)

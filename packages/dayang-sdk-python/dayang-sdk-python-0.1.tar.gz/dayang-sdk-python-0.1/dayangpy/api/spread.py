from dayangpy.api.base import BaseAPI
import datetime


class DaYangSpread(BaseAPI):
    """
    传播分析相关接口
    """

    API_BASE_URL = "http://gateway.bigdata.cloud.dayang.com.cn:8088"

    def create(self, origin_id, title, content):
        """
        批量创建分析任务接口
        """
        result = self._post(
            "/openapi4hoge/v1/path-analysis/tasks",
            data=[{"title": title, "content": content, "id": origin_id}],
        )
        return result.get("resultList", None)

    def task_detail(self, taskId):
        """
        批量查询任务结果接口
        """
        result = self._get(f"/openapi4hoge/v1/path-analysis/task-detail/{taskId}")
        return result.get("resultList", None)

    def article_analysis(self, title, content=""):
        """
        单篇文章传播分析查询
        """
        data = {"title": title, "content": content}
        result = self._post(
            "/openapi4hoge/v1/path-analysis/single-article-analysis", json=data
        )
        return result.get("resultList", None)

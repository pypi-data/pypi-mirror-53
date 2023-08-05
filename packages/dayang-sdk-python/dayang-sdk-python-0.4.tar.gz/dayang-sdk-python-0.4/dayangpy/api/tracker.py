from dayangpy.api.base import BaseAPI


class DaYangTracker(BaseAPI):
    """
    事件跟踪和与事件跟踪分析接口
    """

    API_BASE_URL = "http://gateway.bigdata.cloud.dayang.com.cn:8088"

    def create(self, tracker_type, tracker_name, contain_words, exclude_words=None):
        """
        创建事件跟踪
        """
        tracker_data = {
            "trackerType": tracker_type,
            "trackerName": tracker_name,
            "mustContainWords": contain_words,
            "excludeWords": exclude_words,
        }

        result = self._post("/openapi4hoge/v1/event-tracker/add", json=tracker_data)
        return result.get("result", None)

    def list(self, **kwargs):
        """
        事件跟踪列表
        """
        page = kwargs.get("page", 1)
        page_size = kwargs.get("page_size", 10)
        result = self._get(
            "/openapi4hoge/v1/event-tracker/list",
            params={"page": page, "pageSize": page_size},
        )
        return result.get("result", None).get("datas", None)

    def delete(self, tracker_id):
        """
        删除事件跟踪
        """
        result = self._delete(f"/openapi4hoge/v1/event-tracker/{tracker_id}")
        return result.get("result", None)

    def get_event_tracker_news(self, tracker_id):
        """
        查询新闻汇总接口
        """
        result = self._get(f"/openapi4hoge/v1/event-tracker/event-news/{tracker_id}")
        return result.get("result", None)

    def get_yuqing_trend(self, tracker_id):
        """
        获取事件热度趋势
        """
        result = self._get(f"/openapi4hoge/v1/event/yuqing-trend/{tracker_id}")
        return result.get("resultList", None)

    def get_content_type(self, tracker_id):
        """
        获取事件中文章类型分布
        """
        result = self._get(f"/openapi4hoge/v1/event/content-type/{tracker_id}")
        return result.get("resultList", None)

    def get_hotwords(self, tracker_id):
        """
        获取事件的相关热词
        """
        result = self._get(f"/openapi4hoge/v1/event/hot-words/{tracker_id}")
        return result.get("resultList", None)

    def get_media(self, tracker_id):
        """
        获取事件中媒体传播分布
        """
        result = self._get(f"/openapi4hoge/v1/event/news-media/{tracker_id}")
        return result.get("resultList", None)

    def get_pub_area(self, tracker_id):
        """
        获取发布热区
        """
        result = self._get(f"/openapi4hoge/v1/event/hot-pub-area/{tracker_id}")
        return result.get("resultList", None)

    def get_emotion_attr(self, tracker_id):
        """
        获取情感属性
        """
        result = self._get(f"/openapi4hoge/v1/event/emotion-attr/{tracker_id}")
        return result.get("resultList", None)

    def get_profile(self, tracker_id):
        """
        事件类型的基本信息
        """
        result = self._get(f"/openapi4hoge/v1/event/profile/{tracker_id}")
        return result.get("result", None)

    def get_important_news(self, tracker_id):
        """
        获取重要文章
        """
        result = self._get(f"/openapi4hoge/v1/event/important-news/{tracker_id}")
        return result.get("resultList", None)

    def get_active_media(self, tracker_id):
        """
        获取活跃媒体
        """
        return self._get(f"/openapi4hoge/v1/event/active-media/{tracker_id}")

    def get_refer_area(self, tracker_id):
        """
        获取事件提及热区
        """
        return self._get(f"/openapi4hoge/v1/event/hot-refer-area/{tracker_id}")

    def get_emotion_trend(self, tracker_id):
        """
        获取情感趋势
        """
        return self._get(f"/openapi4hoge/v1/event/emotion-trend/{tracker_id}")

    def get_event_news(self, tracker_id):
        """
        获取事件的文章列表
        """
        result = self._post(f"/openapi4hoge/v1/event/event-news/{tracker_id}")
        return result.get("resultList", None)

    def get_event_news_detail(self, tracker_id, news_uuid):
        """
        获取事件文章详情
        """
        return self._get(f"/openapi4hoge/v1/event/news-detail/{tracker_id}/{news_uuid}")

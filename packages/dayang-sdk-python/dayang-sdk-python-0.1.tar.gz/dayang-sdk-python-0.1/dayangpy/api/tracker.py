from dayangpy.api.base import BaseAPI


class DaYangTracker(BaseAPI):
    """
    事件跟踪和与事件跟踪分析接口
    """

    API_BASE_URL = "http://gateway.bigdata.cloud.dayang.com.cn:8088"

    def create(self, trackerType, trackerName, containWords, excludeWords=None):
        """
        创建事件跟踪
        """
        tracker_data = {
            "trackerType": trackerType,
            "trackerName": trackerName,
            "mustContainWords": containWords,
            "excludeWords": excludeWords,
        }

        result = self._post("/openapi4hoge/v1/event-tracker/add", json=tracker_data)
        return result.get("result", None)

    def list(self, page=None, pageSize=None):
        """
        事件跟踪列表
        """
        result = self._get(
            "/openapi4hoge/v1/event-tracker/list",
            params={"page": page, "pageSize": pageSize},
        )
        return result.get("result", None).get("data", None)

    def delete(self, trackerId):
        """
        删除事件跟踪
        """
        result = self._delete(f"/openapi4hoge/v1/event-tracker/{trackerId}")
        return result.get("result", None)

    def get_event_tracker_news(self, trackerId):
        """
        查询新闻汇总接口
        """
        result = self._get(f"/openapi4hoge/v1/event-tracker/event-news/{trackerId}")
        return result.get("result", None)

    def get_category(self):
        """
        事件类型获取接口
        """
        return self._get("/openapi4hoge/v1/events/classify/list")

    def get_yuqing_trend(self, trackerId):
        """
        获取事件热度趋势
        """
        result = self._get(f"/openapi4hoge/v1/event/yuqing-trend/{trackerId}")
        return result.get("resultList", None)

    def get_content_type(self, trackerId):
        """
        获取事件中文章类型分布
        """
        result = self._get(f"/openapi4hoge/v1/event/content-type/{trackerId}")
        return result.get("resultList", None)

    def get_hotwords(self, trackerId):
        """
        获取事件的相关热词
        """
        result = self._get(f"/openapi4hoge/v1/event/hot-words/{trackerId}")
        return result.get("resultList", None)

    def get_media(self, trackerId):
        """
        获取事件中媒体传播分布
        """
        result = self._get(f"/openapi4hoge/v1/event/news-media/{trackerId}")
        return result.get("resultList", None)

    def get_pub_area(self, trackerId):
        """
        获取发布热区
        """
        result = self._get(f"/openapi4hoge/v1/event/hot-pub-area/{trackerId}")
        return result.get("resultList", None)

    def get_emotion_attr(self, trackerId):
        """
        获取情感属性
        """
        result = self._get(f"/openapi4hoge/v1/event/emotion-attr/{trackerId}")
        return result.get("resultList", None)

    def get_profile(self, trakerId):
        """
        事件类型的基本信息
        """
        result = self._get(f"/openapi4hoge/v1/event/profile/{trakerId}")
        return result.get("result", None)

    def get_important_news(self, trackerId):
        """
        获取重要文章
        """
        result = self._get(f"/openapi4hoge/v1/event/important-news/{trackerId}")
        return result.get("resultList", None)

    def get_active_media(self, trackerId):
        """
        获取活跃媒体
        """
        return self._get(f"/openapi4hoge/v1/event/active-media/{trackerId}")

    def get_refer_area(self, trackerId):
        """
        获取事件提及热区
        """
        return self._get(f"/openapi4hoge/v1/event/hot-refer-area/{trackerId}")

    def get_emotion_trend(self, trackerId):
        """
        获取情感趋势
        """
        return self._get(f"/openapi4hoge/v1/event/emotion-trend/{trackerId}")

    def get_event_news(self, trackerId):
        """
        获取事件的文章列表
        """
        result = self._post(f"/openapi4hoge/v1/event/event-news/{trackerId}")
        return result.get("resultList", None)

    def get_event_news_detail(self, trackerId, news_uuid):
        """
        获取事件文章详情
        """
        return self._get(f"/openapi4hoge/v1/event/news-detail/{trackerId}/{news_uuid}")

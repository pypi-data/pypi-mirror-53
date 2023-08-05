class BaseAPI(object):
    """DaYang API base class """

    def __init__(self, client=None):
        self._client = client

    def _get(self, url, **kwargs):
        if getattr(self, "API_BASE_URL", None):
            kwargs["api_base_url"] = self.API_BASE_URL
        headers = {"token": self._client.access_token}
        return self._client.get(url, headers=headers, **kwargs)

    def _post(self, url, **kwargs):
        if getattr(self, "API_BASE_URL", None):
            kwargs["api_base_url"] = self.API_BASE_URL
        headers = {
            "Content-Type": "application/json",
            "token": self._client.access_token,
        }
        return self._client.post(url, headers=headers, **kwargs)

    def _delete(self, url, **kwargs):
        if getattr(self, "API_BASE_URL", None):
            kwargs["api_base_url"] = self.API_BASE_URL
        headers = {"token": self._client.access_token}
        return self._client.delete(url, headers=headers, **kwargs)

    @property
    def access_token(self):
        return self._client.access_token

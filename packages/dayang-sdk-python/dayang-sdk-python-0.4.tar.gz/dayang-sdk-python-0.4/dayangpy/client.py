import inspect
import requests
from dayangpy.exceptions import BaseException
from dayangpy.api.base import BaseAPI
import json


def _is_api_endpoint(obj):
    return isinstance(obj, BaseAPI)


class BaseClient(object):
    API_BASE_URL = ""

    def __new__(cls, *args, **kwargs):
        self = super(BaseClient, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self)
            setattr(self, name, api)
        return self

    def __init__(self, tenant_id, user_id, client_id, client_secret, access_token=None):

        self._http = requests.Session()
        self.tenantId = tenant_id
        self.userId = user_id
        self.client_id = client_id
        self.client_secret = client_secret

    def _request(self, method, url_or_endpoint, **kwargs):
        """
         处理request
        """
        if not url_or_endpoint.startswith(("http://", "https://")):
            api_base_url = kwargs.pop("api_base_url", self.API_BASE_URL)
            url = f"{api_base_url}{url_or_endpoint}"
        else:
            url = url_or_endpoint

        try:
            res = self._http.request(timeout=15, method=method, url=url, **kwargs)
            res.raise_for_status()
            data = res.json()

        except json.JSONDecodeError as e:
            raise res.text

        except requests.RequestException as reqe:
            raise reqe

        return self._handle_result(data)

    def _handle_result(self, data):
        """
        处理result
        """
        if not isinstance(data, dict):
            result = self._decode_result(data)
        else:
            result = data

        if data.get("success") == False:
            raise BaseException(data)

        return result

    def _decode_result(self, res):
        """
        reuslt转字典
        """
        try:
            result = json.loads(res.content.decode("utf-8", "ignore"), strict=False)
        except (TypeError, ValueError):
            return res
        return result

    def get(self, url, **kwargs):
        return self._request(method="get", url_or_endpoint=url, **kwargs)

    def post(self, url, **kwargs):
        return self._request(method="post", url_or_endpoint=url, **kwargs)

    def delete(self, url, **kwargs):
        return self._request(method="delete", url_or_endpoint=url, **kwargs)

    def _fetch_access_token(self, url, **kwargs):
        res = self._http.post(url=url, **kwargs)
        result = res.json()
        access_token = result["access_token"]
        return access_token

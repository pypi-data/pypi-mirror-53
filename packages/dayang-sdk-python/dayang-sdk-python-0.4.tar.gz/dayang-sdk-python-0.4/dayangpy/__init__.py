from __future__ import absolute_import, unicode_literals
import base64
from dayangpy import api
from dayangpy.client import BaseClient

class Client(BaseClient):

    """
    """

    API_BASE_URL = "http://gateway.bigdata.cloud.dayang.com.cn:8088"

    tracker = api.DaYangTracker()
    hotspot = api.DaYangHotspot()
    rank = api.DaYangRank()
    platform = api.DaYangPlatform()
    news = api.DaYangNews()
    spread = api.DaYangSpread()

    def __init__(self, tenant_id, user_id, client_id, client_secret, access_token=None):
        super(Client, self).__init__(
            tenant_id, user_id, client_id, client_secret, access_token
        )
        self.tenantId = tenant_id
        self.userId = user_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.fetch_access_token(self.client_id, self.client_secret)

    def fetch_access_token(self, client_id, client_secret):
        """
        获取 access token
        """
        auth = base64.b64encode((client_id + ":" + client_secret).encode())
        return self._fetch_access_token(
            url="http://gateway.bigdata.cloud.dayang.com.cn:8088/oauth/token",
            params={
                "grant_type": "client_credentials",
                "tenantId": self.tenantId,
                "userId": self.userId,
            },
            headers={"Authorization": "Basic {}".format(bytes.decode(auth))},
        )

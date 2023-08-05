from unittest import TestCase
from test.rikki.mitmproxy.utils import build_flow
from rikki.mitmproxy.model import Request
from rikki.mitmproxy.util import filter


class TestFlowFilter(TestCase):

    def test_plain_host(self):
        flow = build_flow(request=Request(host="www.google.com"))

        result = filter([flow], request=Request(host="google"))

        assert len(result) == 0

        result = filter([flow], request=Request(host=".*google"))

        assert len(result) == 0

        result = filter([flow], request=Request(host=".*google.*"))

        assert len(result) == 1

    def test_plain_host_and_host_header(self):
        flow = build_flow(request=Request(host="127.0.0.1", headers={"Host": "www.google.com"}))

        result = filter([flow], request=Request(host="google"))

        assert len(result) == 0

        result = filter([flow], request=Request(host=".*google"))

        assert len(result) == 0

        result = filter([flow], request=Request(host=".*google.*"))

        assert len(result) == 1

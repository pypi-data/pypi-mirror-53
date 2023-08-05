from mitmproxy import http
from rikki.mitmproxy.model import Request, Response
from typing import List, Optional, Dict
from mitmproxy.coretypes import multidict
from mitmproxy.net.http import Headers
import json
import re


def is_json(content: str):
    try:
        json.loads(content)
    except ValueError:
        return False
    return True


def is_html(content: str):
    if content.lower().startswith("<!DOCTYPE html>".lower()):
        return True
    else:
        return False


def content_type(content: str) -> str:
    if is_json(content):
        return "application/json; charset=UTF-8"
    elif is_html(content):
        return "text/html; charset=utf-8"
    else:
        return "text/plain"


def replace(flow: http.HTTPFlow, request: Optional[Request] = None, response: Optional[Response] = None):
    if request:
        if request.host:
            flow.request.host = request.host
        if request.content:
            flow.request.content = request.content.encode("utf8")
        if request.params:
            for item in request.params.items():
                flow.request.query.set_all(item[0], [item[1]])
        if request.headers:
            for item in request.headers.items():
                headers: Headers = flow.request.headers
                headers.set_all(item[0], [item[1]])
    if response:
        if response.headers:
            for item in response.headers.items():
                headers: Headers = flow.response.headers
                headers.set_all(item[0], [item[1]])
        if response.content:
            flow.response.content = response.content.encode("utf8")
            flow.response.headers["Content-Type"] = content_type(response.content)
        if response.code:
            flow.response.status_code = response.code


def filter(
        flows: List[http.HTTPFlow],
        request: Optional[Request] = None,
        response: Optional[Response] = None
) -> List[http.HTTPFlow]:
    """
    Filter flows and return only those that contain data from filter params
    :param flows: list of flows to be filtered
    :param request: request data to look for during filter
    :param response: response data to look for during filter
    :return: new list of filtered flows
    """
    result: List[http.HTTPFlow] = []
    result.extend(flows)

    for flow in result:
        if request:
            if request.port and request.port != flow.request.port:
                if flow in result:
                    result.remove(flow)
                continue
            if request.path and request.path != flow.request.path.split("?")[0]:
                if flow in result:
                    result.remove(flow)
                continue
            if request.host:
                host_pattern = re.compile("{0}".format(request.host))
                """
                Use `Host` header as fallback when proxy works as transparent proxy and has only ip addresses
                """
                request_host = flow.request.host
                header_host = ""
                host_header_name = 'Host'
                if host_header_name in flow.request.headers:
                    header_host = flow.request.headers[host_header_name]
                if not host_pattern.fullmatch(request_host) and not host_pattern.fullmatch(header_host):
                    if flow in result:
                        result.remove(flow)
            if request.params and not contains_params(flow.request.query, request.params):
                if flow in result:
                    result.remove(flow)
                continue
            if request.content and not request.content.lower().strip() != flow.request.content.lower().strip():
                if flow in result:
                    result.remove(flow)
            if request.headers and not contains_headers(flow.request.headers, request.headers):
                if flow in result:
                    result.remove(flow)
        if response:
            if response.code and response.code != flow.response.status_code:
                if flow in result:
                    result.remove(flow)
            if response.headers and not contains_headers(flow.response.headers, response.headers):
                if flow in result:
                    result.remove(flow)
            if response.content and flow.response.content \
                    and response.content.lower().strip() != flow.response.content.decode("utf8").lower().strip():
                if flow in result:
                    result.remove(flow)

    return result


def contains_params(base: multidict.MultiDictView, candidate: Dict) -> bool:
    for key in candidate.keys():
        if key in base.keys() and candidate[key] in base.get_all(key):
            continue
        else:
            return False
    return True


def contains_headers(headers: Headers, candidate: Dict[str, str]):
    for key in candidate.keys():
        if key in headers.keys() and candidate[key] in headers.get_all(key):
            continue
        else:
            return False
    return True

"""
refer to:
"""
from collections import namedtuple
from enum import Enum
from typing import Tuple, Dict

from flask import jsonify as jy

error_structure = namedtuple('error_structure', ['http_status_code', 'error_code', 'error_message'])


class CommonError(Enum):
    internal_server_error = error_structure(500, 'InternalServerError', '服务器内部错误')
    signature_not_match = error_structure(401, 'SignatureNotMatch', '请求的数字签名不匹配')
    unauthorized = error_structure(401, 'Unauthorized', '未授权操作')
    # 不要笼统的设置参数错误，而是具体说明哪个参数错误. 参数错误 http_status_code 是 400.


def _check_error_response(data, http_code):
    if http_code != 200 and not isinstance(data, error_structure):
        raise TypeError(f'the type of data {data} is not error_structure')


def _convert_asdict(data: namedtuple) -> Dict:
    return data._asdict()


def jsonify(data, http_code=200) -> Tuple:
    _check_error_response(data, http_code)
    if isinstance(data, error_structure):
        data = _convert_asdict(data)
    return jy(data), http_code

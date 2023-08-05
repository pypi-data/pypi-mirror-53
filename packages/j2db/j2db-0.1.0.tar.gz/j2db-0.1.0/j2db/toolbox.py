import json

from j2db import constants


def is_json_valid(content: str) -> bool:
    try:
        json.loads(content, encoding=constants.CHARSET)
    except ValueError:
        return False
    else:
        return True


def json2dict(content: str) -> dict:
    return json.loads(content, encoding=constants.CHARSET)

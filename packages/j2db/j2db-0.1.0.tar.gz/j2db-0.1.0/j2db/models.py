from pydantic import BaseModel
import json

from j2db import toolbox


class JsonRequestModel(BaseModel):
    """ for parsing args of request only """

    # for matching models
    table: str = ""
    # action
    action: str = ""
    # json
    content: str = ""
    # secret
    secret: str = ""


class EventModel(object):
    """ all the requests should be converted to this type, and sent to handler """

    def __init__(self, table: str, action: str, content: str, secret: str):
        self.table = table
        self.action = action
        self.content = content
        self.secret = secret

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return json.dumps(self.__dict__)

    def is_content_valid(self) -> bool:
        # "123" is valid json
        # but "abc" is not
        try:
            int(self.content)
        except ValueError:
            pass
        else:
            return False
        return toolbox.is_json_valid(self.content)

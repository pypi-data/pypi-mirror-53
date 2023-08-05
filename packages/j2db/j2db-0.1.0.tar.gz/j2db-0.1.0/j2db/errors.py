import typing

from j2db.models import EventModel


def auth_invalid_error(origin_request: EventModel) -> typing.Dict[str, str]:
    return {
        "error": "auth_invalid",
        "msg": "auth failed, check your secret",
        "request": origin_request.to_dict(),
        "stack": "",
    }


def json_invalid_error(origin_request: EventModel) -> typing.Dict[str, str]:
    return {
        "error": "json_invalid",
        "msg": "content in your request is not a valid json format",
        "request": origin_request.to_dict(),
        "stack": "",
    }


def table_invalid_error(origin_request: EventModel) -> typing.Dict[str, str]:
    return {
        "error": "table_invalid",
        "msg": "should match the table name",
        "request": origin_request.to_dict(),
        "stack": "",
    }


def db_operator_error(origin_request: EventModel, error: str) -> typing.Dict[str, str]:
    return {
        "error": "db_operator",
        "msg": "operate failed",
        "request": origin_request.to_dict(),
        "stack": error,
    }


AuthInvalidError = auth_invalid_error
JsonInvalidError = json_invalid_error
TableInvalidError = table_invalid_error
DBOperatorError = db_operator_error

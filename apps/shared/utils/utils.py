from rest_framework import status
from rest_framework.response import Response

from apps.shared.utils.result_codes import ResultCodes, ResultMessages


def success_response(result=None, status_code=status.HTTP_200_OK):
    if isinstance(result, ResultCodes):
        return Response(
            {
                "success": True,
                "result": {
                    "code": result.value,
                    "message": ResultMessages[result.name]["en"],
                    "message_language": {
                        "uz": ResultMessages[result.name]["uz"],
                        "en": ResultMessages[result.name]["en"],
                        "ru": ResultMessages[result.name]["ru"],
                    },
                },
            },
            status=status_code,
        )
    return Response({"success": True, "result": result}, status=status_code)


def error_response(
    result: ResultCodes,
    message: dict[str, str] | None = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    data: dict | None = None,
) -> Response:
    err_body = {
        "code": result.value,
        "message": message["en"] if message else ResultMessages[result.name]["en"],
        "message_language": {
            "uz": message["uz"] if message else ResultMessages[result.name]["uz"],
            "en": message["en"] if message else ResultMessages[result.name]["en"],
            "ru": message["ru"] if message else ResultMessages[result.name]["ru"],
        },
    }
    if data:
        err_body.update(data)

    return Response(
        {
            "success": False,
            "error": err_body,
        },
        status=status_code,
    )

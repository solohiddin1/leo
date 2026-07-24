from rest_framework import status
from rest_framework.response import Response

from apps.shared.utils.result_codes import ResultCodes, ResultMessages


def success_response(result=None, status_code=status.HTTP_200_OK):
    return Response({
        "success": True,
        "result": result
    }, status=status_code)

def error_response(
    result: ResultCodes,
    message: dict[str, str] | None = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Response:
    if message:
        return Response({
            "success": False,
            "error": {
                "code": result.value,
                "message": message["en"],
                "message_language": {
                    "uz": message["uz"],
                    "en": message["en"],
                    "ru": message["ru"],
                }
            }
        }, status=status_code)

    return Response({
        "success": False,
        "error": {
            "code": result.value,
            "message": ResultMessages[result.name]["en"],
            "message_language": {
                "uz": ResultMessages[result.name]["uz"],
                "en": ResultMessages[result.name]["en"],
                "ru": ResultMessages[result.name]["ru"],
            }
        }
    }, status=status_code)

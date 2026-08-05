from rest_framework.exceptions import Throttled
from rest_framework.response import Response
from apps.shared.utils.utils import ResultCodes, ResultMessages
from rest_framework.views import exception_handler

def get_messages(code: ResultCodes, **args) -> dict:
    messages = ResultMessages.get(code.name, {})
    result = {}
    for lang, template in messages.items():
        try:
            result[lang] = template.format(**args) if args else template
        except (KeyError, IndexError):
            result[lang] = template
    return result

def custom_exception_handler(exc, context):
    if isinstance(exc, Throttled):
        wait = int(exc.wait or 0)
        code = getattr(exc, "result_code", ResultCodes.TOO_MANY_REQUESTS)
        return Response(
            {
                "code": code.name.lower(),
                "message": get_messages(code, wait=wait),
                "args": {"wait": wait},
            },
            status=429,
        )
    return exception_handler(exc, context)
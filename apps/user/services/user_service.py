from apps.user.models import User
from apps.shared.utils.utils import success_response
from apps.user.api.serializers.register import RegisterSerializer

class UserService:
    @staticmethod
    def register(data: dict) -> User:
        user = User.objects.create_user(**data)
        user.save()
        data = RegisterSerializer(user).data
        return success_response(data)

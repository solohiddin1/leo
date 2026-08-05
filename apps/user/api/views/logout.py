from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import User
from apps.shared.security import GeneralThrottle
from apps.user.api.serializers.logout import LogoutSerializer
from shared.permission.client import ClientPermission
from shared.utils.result_codes import ResultCodes
from shared.utils.utils import error_response, success_response


class LogoutAPIView(GenericAPIView):
	queryset = User.objects.all()
	serializer_class = LogoutSerializer
	permission_classes = [ClientPermission]
	throttle_classes = [GeneralThrottle]

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		try:
			RefreshToken(serializer.validated_data['refresh_token']).blacklist()
		except TokenError:
			return error_response(ResultCodes.INVALID_TOKEN_ERROR)
		return success_response()

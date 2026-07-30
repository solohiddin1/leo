from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

@method_decorator(staff_member_required, name='dispatch')
class ProtectedSpectacularSwaggerView(SpectacularSwaggerView):
    pass

@method_decorator(staff_member_required, name='dispatch')
class ProtectedSpectacularRedocView(SpectacularRedocView):
    pass

@method_decorator(staff_member_required, name='dispatch')
class ProtectedSpectacularAPIView(SpectacularAPIView):
    pass
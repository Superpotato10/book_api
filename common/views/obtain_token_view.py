from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.views import ObtainAuthToken


@extend_schema(tags=['Authorization'])
class ObtainTokenView(ObtainAuthToken):
    ...

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .mmodels import Device

class DeviceTokenAuthentication(BaseAuthentication):
    def authentication(self, request):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Token '):
            return none 

        token = token.split(' ')[1]
        try:
            device = Device.objects.get(token=token)
        except Device.DoesNotExist:
            raise AuthenticationFailed('Invalid device token')

        return (device.owner, device)
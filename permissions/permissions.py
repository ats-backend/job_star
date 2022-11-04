import hashlib

from decouple import config
from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        API_KEY = request.META.get('HTTP_API_KEY')
        request_ts = request.META.get('HTTP_REQUEST_TS')
        hash_key = request.META.get('HTTP_HASH_KEY')
        local_api_key = config('API_KEY')
        local_secret_key = config('SECRET_KEY')
        try:
            de_hash = local_api_key + local_secret_key + request_ts
        except:
            return False
        hash = hashlib.sha256(de_hash.encode('utf8')).hexdigest()

        if hash != hash_key:
            return False

        return True

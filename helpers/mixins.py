from rest_framework.generics import CreateAPIView, UpdateAPIView

from job_star.encryption import decrypt_data


class DecryptionMixin(CreateAPIView, UpdateAPIView):

    def post(self, request, *args, **kwargs):
        if request.data.get('data'):
            try:
                dec_data = decrypt_data(request.data['data'])
                request._full_data = dec_data
            except:
                request._full_data = request.data

        return super(DecryptionMixin, self).post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if request.data.get('data'):
            try:
                dec_data = decrypt_data(request.data['data'])
                request._full_data = dec_data
            except:
                request._full_data = request.data

        return super(DecryptionMixin, self).put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if request.data.get('data'):
            try:
                dec_data = decrypt_data(request.data['data'])
                request._full_data = dec_data
            except:
                request._full_data = request.data

        return super(DecryptionMixin, self).patch(request, *args, **kwargs)
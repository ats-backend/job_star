from rest_framework import serializers

from .models import Job


class JobSerializers(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = (
            'title', 'description', 'responsibilities',
            'requirement', 'date_posted', 'deadline'
        )

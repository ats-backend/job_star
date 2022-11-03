import datetime
import pytz

utc = pytz.UTC

from rest_framework import serializers

from .models import Job


class JobSerializers(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = (
            'id', 'title', 'description', 'responsibilities',
            'requirement', 'date_posted', 'deadline'
        )

    def validate(self, attrs):
        jobs = Job.objects.values_list('title')
        if any(attrs['title'] in title for title in jobs):
            raise serializers.ValidationError({
                'title: A job with that title is already exist'
            })

        if attrs['deadline'] < utc.localize(datetime.datetime.now()):
            raise serializers.ValidationError({
                'date_posted': "creation date and deadline can not be greater than"
                               "today's date",
            })
        return attrs